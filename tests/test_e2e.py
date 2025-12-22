"""
End-to-End Integration Tests

These tests run against real UCMDB servers and perform complete workflows
including create, verify, update, and delete operations.

WARNING: These tests will create and delete resources on the UCMDB server.
Only run against dedicated test/development servers - NEVER production!

Usage:
    # Set environment variable to enable E2E tests
    export UCMDB_E2E_TESTS=true

    # Run E2E tests
    python -m pytest tests/test_e2e.py -v

    # Or use the test runner
    python tests/run_tests.py --e2e

Requirements:
    - ucmdb_rest/discovery/credentials.json with test server details
    - Test servers must be "crash and burn" environments (non-production)
"""

import unittest
import uuid
import time
import json
import os
import sys
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings for cleaner test output
# Note: The library uses verify=False for UCMDB connections
warnings.filterwarnings('ignore', category=InsecureRequestWarning)
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import ucmdb_rest.utils as utils
import ucmdb_rest.datamodel as datamodel
import ucmdb_rest.topology as topology
import ucmdb_rest.discovery as discovery
import ucmdb_rest.settings as settings

# Check if E2E tests are enabled
E2E_ENABLED = os.environ.get('UCMDB_E2E_TESTS', 'false').lower() == 'true'


def load_test_credentials():
    """Load test server credentials from credentials.json"""
    cred_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        'ucmdb_rest',
        'discovery',
        'credentials.json'
    )

    if not os.path.exists(cred_file):
        raise FileNotFoundError(
            f"Credentials file not found: {cred_file}\n"
            "Please create ucmdb_rest/discovery/credentials.json"
        )

    with open(cred_file, 'r') as f:
        config = json.load(f)

    # Use first server for E2E tests
    if not config.get('servers'):
        raise ValueError("No servers configured in credentials.json")

    return config['servers'][0]


class BaseE2ETest(unittest.TestCase):
    """Base class for E2E tests with setup/teardown"""

    @classmethod
    def setUpClass(cls):
        """Set up test server connection once for all tests"""
        if not E2E_ENABLED:
            raise unittest.SkipTest("E2E tests disabled (set UCMDB_E2E_TESTS=true)")

        try:
            server = load_test_credentials()
            cls.server = server['hostname']
            cls.port = server['port']
            cls.username = server['username']
            cls.password = server['password']
            cls.version = server['version']

            # Create authentication token
            cls.token = utils.createHeaders(cls.username, cls.password, cls.server, port=cls.port)

            print(f"\nE2E Tests running against UCMDB {cls.version} @ {cls.server}:{cls.port}")

        except Exception as e:
            raise unittest.SkipTest(f"Failed to connect to test server: {e}")

    def setUp(self):
        """Set up for each test - create unique identifiers"""
        self.test_id = str(uuid.uuid4())[:8]  # Short UUID for readability
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.created_resources = []  # Track resources for cleanup

    def tearDown(self):
        """Clean up any resources created during the test"""
        # Cleanup happens in individual test methods
        # This is a safety net in case test fails before cleanup
        pass

    def generate_unique_name(self, base_name):
        """Generate unique name for test resources"""
        return f"{base_name}_test_{self.timestamp}_{self.test_id}"


class TestCIOperations(BaseE2ETest):
    """Test complete CI lifecycle: Create → Query → Update → Delete"""

    def test_01_create_verify_delete_simple_ci(self):
        """Test: Create single CI, verify it exists, then delete it"""

        # Step 1: Create a test CI with unique name
        test_ci_name = self.generate_unique_name("node")
        test_ci_fqdn = f"{test_ci_name}.test.ucmdb.local"

        ci_to_create = {
            "cis": [
                {
                    "ucmdbId": "1",
                    "type": "node",
                    "properties": {
                        "name": test_ci_name,
                        "primary_dns_name": test_ci_fqdn,
                        "os_family": "windows"
                    }
                }
            ],
            "relations": []
        }

        print(f"\n  Creating CI: {test_ci_name}")
        create_response = datamodel.addCIs(self.token, self.server, ci_to_create, returnIdsMap=True)
        self.assertEqual(create_response.status_code, 200,
                        f"Failed to create CI: {create_response.text}")

        # Extract the real UCMDB ID from the response using idsMap
        create_data = create_response.json()
        actual_ci_id = None
        if 'idsMap' in create_data and '1' in create_data['idsMap']:
            actual_ci_id = create_data['idsMap']['1']

        self.assertIsNotNone(actual_ci_id, f"Failed to get CI ID from create response: {create_data}")
        print(f"  Created CI with ID: {actual_ci_id}")

        # Step 2: Query to verify the CI exists
        time.sleep(2)  # Give UCMDB time to index the CI

        query = {
            "nodes": [
                {
                    "type": "node",
                    "queryIdentifier": "node",
                    "visible": "true",
                    "includeSubtypes": "false",
                    "layout": ["name", "primary_dns_name"],
                    "attributeConditions": [
                        {
                            "attribute": "name",
                            "operator": "like",
                            "value": test_ci_name
                        }
                    ],
                    "linkConditions": [],
                    "ids": []
                }
            ],
            "relations": []
        }

        print(f"  Querying for CI: {test_ci_name}")
        query_response = topology.queryCIs(self.token, self.server, query)
        self.assertEqual(query_response.status_code, 200,
                        f"Failed to query CI: {query_response.text}")

        query_data = query_response.json()
        found_cis = query_data.get('cis', [])
        self.assertGreater(len(found_cis), 0, f"CI {test_ci_name} not found in query results")

        # Verify the CI has the correct properties
        found_ci = found_cis[0]
        self.assertEqual(found_ci['properties'].get('name'), test_ci_name)
        self.assertEqual(found_ci['properties'].get('primary_dns_name'), test_ci_fqdn)
        print(f"  Verified CI exists with correct properties")

        # Step 3: Delete the CI
        print(f"  Deleting CI: {actual_ci_id}")
        delete_response = datamodel.deleteCIs(self.token, self.server,actual_ci_id)
        self.assertEqual(delete_response.status_code, 200,
                        f"Failed to delete CI: {delete_response.text}")
        print(f"  Successfully deleted CI")

        # Step 4: Verify CI is gone
        time.sleep(2)  # Give UCMDB time to process deletion

        query_response2 = topology.queryCIs(self.token, self.server, query)
        self.assertEqual(query_response2.status_code, 200)

        query_data2 = query_response2.json()
        found_cis2 = query_data2.get('cis', [])
        self.assertEqual(len(found_cis2), 0,
                        f"CI {test_ci_name} still exists after deletion")
        print(f"  Verified CI was deleted")

    def test_02_create_update_delete_ci(self):
        """Test: Create CI, update its properties, verify update, then delete"""

        # Step 1: Create CI
        test_ci_name = self.generate_unique_name("node")
        test_ci_fqdn = f"{test_ci_name}.test.ucmdb.local"

        ci_to_create = {
            "cis": [
                {
                    "ucmdbId": "1",
                    "type": "node",
                    "properties": {
                        "name": test_ci_name,
                        "primary_dns_name": test_ci_fqdn,
                        "os_family": "windows"
                    }
                }
            ],
            "relations": []
        }

        print(f"\n  Creating CI: {test_ci_name}")
        create_response = datamodel.addCIs(self.token, self.server, ci_to_create, returnIdsMap=True)
        self.assertEqual(create_response.status_code, 200)

        create_data = create_response.json()
        actual_ci_id = create_data['idsMap']['1'] if 'idsMap' in create_data else None
        self.assertIsNotNone(actual_ci_id)
        print(f"  Created CI with ID: {actual_ci_id}")

        time.sleep(2)

        # Step 2: Update the CI (change os_family)
        ci_update = {
            "properties": {
                "os_family": "unix"
            }
        }

        print(f"  Updating CI os_family to 'unix'")
        update_response = datamodel.updateCI(self.token, self.server, actual_ci_id, ci_update)
        self.assertEqual(update_response.status_code, 200,
                        f"Failed to update CI: {update_response.text}")
        print(f"  Successfully updated CI")

        # Step 3: Query to verify the update
        time.sleep(2)

        query = {
            "nodes": [
                {
                    "type": "node",
                    "queryIdentifier": "node",
                    "visible": "true",
                    "includeSubtypes": "false",
                    "layout": ["name", "os_family"],
                    "attributeConditions": [
                        {
                            "attribute": "name",
                            "operator": "like",
                            "value": test_ci_name
                        }
                    ],
                    "linkConditions": [],
                    "ids": []
                }
            ],
            "relations": []
        }

        print(f"  Verifying update...")
        query_response = topology.queryCIs(self.token, self.server, query)
        self.assertEqual(query_response.status_code, 200)

        query_data = query_response.json()
        found_ci = query_data.get('cis', [])[0]
        self.assertEqual(found_ci['properties'].get('os_family'), 'unix',
                        "CI update was not applied")
        print(f"  Verified os_family was updated to 'unix'")

        # Step 4: Clean up - delete CI
        print(f"  Deleting CI: {actual_ci_id}")
        delete_response = datamodel.deleteCIs(self.token, self.server,actual_ci_id)
        self.assertEqual(delete_response.status_code, 200)
        print(f"  Successfully deleted CI")

    def test_03_create_bulk_cis_and_cleanup(self):
        """Test: Create multiple CIs in bulk, verify count, then delete all"""

        # Step 1: Create 10 test CIs
        base_name = self.generate_unique_name("bulk_node")
        num_cis = 10

        ci_list = []
        for i in range(num_cis):
            ci_name = f"{base_name}_{i}"
            ci_list.append({
                "ucmdbId": str(i),
                "type": "node",
                "properties": {
                    "name": ci_name,
                    "primary_dns_name": f"{ci_name}.test.ucmdb.local"
                }
            })

        bulk_create = {
            "cis": ci_list,
            "relations": []
        }

        print(f"\n  Creating {num_cis} CIs with base name: {base_name}")
        create_response = datamodel.addCIs(self.token, self.server, bulk_create, returnIdsMap=True)
        self.assertEqual(create_response.status_code, 200,
                        f"Failed to create bulk CIs: {create_response.text}")

        create_data = create_response.json()
        created_ids = list(create_data.get('idsMap', {}).values())
        self.assertEqual(len(created_ids), num_cis,
                        f"Expected {num_cis} CIs, got {len(created_ids)}")
        print(f"  Created {len(created_ids)} CIs")

        time.sleep(3)  # Give UCMDB time to index all CIs

        # Step 2: Query to verify all CIs exist
        query = {
            "nodes": [
                {
                    "type": "node",
                    "queryIdentifier": "node",
                    "visible": "true",
                    "includeSubtypes": "false",
                    "layout": ["name"],
                    "attributeConditions": [
                        {
                            "attribute": "name",
                            "operator": "like",
                            "value": f"{base_name}%"
                        }
                    ],
                    "linkConditions": [],
                    "ids": []
                }
            ],
            "relations": []
        }

        print(f"  Querying for CIs starting with: {base_name}")
        query_response = topology.queryCIs(self.token, self.server, query)
        self.assertEqual(query_response.status_code, 200)

        query_data = query_response.json()
        found_cis = query_data.get('cis', [])
        self.assertEqual(len(found_cis), num_cis,
                        f"Expected {num_cis} CIs in query, found {len(found_cis)}")
        print(f"  Verified all {len(found_cis)} CIs exist")

        # Step 3: Clean up - delete all CIs
        print(f"  Deleting {len(created_ids)} CIs...")
        for ci_id in created_ids:
            delete_response = datamodel.deleteCIs(self.token, self.server,ci_id)
            self.assertEqual(delete_response.status_code, 200,
                           f"Failed to delete CI {ci_id}")
        print(f"  Successfully deleted all {len(created_ids)} CIs")


class TestJobGroupOperations(BaseE2ETest):
    """Test job group lifecycle: Create → Verify → Delete"""

    def test_01_create_verify_delete_job_group(self):
        """Test: Create job group, verify it exists, then delete it"""

        # Step 1: Create test job group
        job_group_name = self.generate_unique_name("test_job_group")

        job_group = {
            "name": job_group_name,
            "type": "CMS",
            "oob": False,
            "description": f"Test job group created by E2E test at {self.timestamp}",
            "discoveryType": None,
            "jobs": [
                {
                    "jobName": "Call Home Processing",
                    "jobDisplayName": "Call Home Processing",
                    "adapterName": "CallHomeProcessing",
                    "inputCI": "callhome_event",
                    "jobType": "DynamicService",
                    "protocols": [],
                    "jobParameters": {},
                    "triggerQueries": [],
                    "jobInvokeOnNewTrigger": True
                }
            ]
        }

        print(f"\n  Creating job group: {job_group_name}")
        create_response = discovery.createJobGroup(self.token, self.server, job_group)
        self.assertEqual(create_response.status_code, 200,
                        f"Failed to create job group: {create_response.text}")
        print(f"  Created job group successfully")

        time.sleep(2)

        # Step 2: Verify job group exists
        print(f"  Verifying job group exists...")
        get_response = discovery.getJobGroup(self.token, self.server)
        self.assertEqual(get_response.status_code, 200)

        job_groups = get_response.json()
        existing_jobs = []
        for key in job_groups:
            if isinstance(job_groups[key], list):
                for job in job_groups[key]:
                    if isinstance(job, dict) and 'id' in job:
                        existing_jobs.append(job['id'])

        self.assertIn(job_group_name, existing_jobs,
                     f"Job group {job_group_name} not found in list")
        print(f"  Verified job group exists")

        # Step 3: Delete job group
        print(f"  Deleting job group: {job_group_name}")
        delete_response = discovery.deleteSpecificJobGroup(self.token, self.server, job_group_name)
        self.assertEqual(delete_response.status_code, 200,
                        f"Failed to delete job group: {delete_response.text}")
        print(f"  Successfully deleted job group")

        # Step 4: Verify deletion
        time.sleep(2)

        get_response2 = discovery.getJobGroup(self.token, self.server)
        self.assertEqual(get_response2.status_code, 200)

        job_groups2 = get_response2.json()
        existing_jobs2 = []
        for key in job_groups2:
            if isinstance(job_groups2[key], list):
                for job in job_groups2[key]:
                    if isinstance(job, dict) and 'id' in job:
                        existing_jobs2.append(job['id'])

        self.assertNotIn(job_group_name, existing_jobs2,
                        f"Job group {job_group_name} still exists after deletion")
        print(f"  Verified job group was deleted")


class TestRecipientOperations(BaseE2ETest):
    """Test recipient lifecycle: Create → Update → Delete"""

    def test_01_create_update_delete_recipient(self):
        """Test: Create recipient, update it, verify update, then delete"""

        # Step 1: Create test recipient
        recipient_name = self.generate_unique_name("test_recipient")
        recipient_email = f"{recipient_name}@test.ucmdb.local"

        recipient = {
            "name": recipient_name,
            "addresses": [recipient_email],
            "id": ""
        }

        print(f"\n  Creating recipient: {recipient_name}")
        create_response = settings.addRecipients(self.token, self.server, recipient)
        self.assertEqual(create_response.status_code, 200,
                        f"Failed to create recipient: {create_response.text}")

        create_data = create_response.json()
        # Extract recipient ID from response
        recipient_id = create_data.get('id') or recipient_name
        print(f"  Created recipient with ID: {recipient_id}")

        time.sleep(2)

        # Step 2: Verify recipient exists
        print(f"  Verifying recipient exists...")
        get_response = settings.getRecipients(self.token, self.server)
        self.assertEqual(get_response.status_code, 200)

        recipients = get_response.json()
        recipient_names = [r.get('name') for r in recipients if isinstance(r, dict)]
        self.assertIn(recipient_name, recipient_names,
                     f"Recipient {recipient_name} not found")
        print(f"  Verified recipient exists")

        # Step 3: Update recipient (change email addresses)
        new_email = f"{recipient_name}_updated@test.ucmdb.local"
        update_data = {
            "addresses": [new_email]
        }

        print(f"  Updating recipient email to: {new_email}")
        update_response = settings.updateRecipients(self.token, self.server, recipient_id, update_data)
        self.assertEqual(update_response.status_code, 200,
                        f"Failed to update recipient: {update_response.text}")
        print(f"  Successfully updated recipient")

        # Step 4: Verify update
        time.sleep(2)

        get_response2 = settings.getRecipients(self.token, self.server)
        self.assertEqual(get_response2.status_code, 200)

        recipients2 = get_response2.json()

        # Find recipient by ID (name might be cleared after update)
        updated_recipient = next(
            (r for r in recipients2 if isinstance(r, dict) and r.get('id') == recipient_id),
            None
        )

        self.assertIsNotNone(updated_recipient,
                           f"Updated recipient not found by ID: {recipient_id}")
        self.assertIn(new_email, updated_recipient.get('addresses', []),
                     "Recipient email was not updated")
        print(f"  Verified email was updated")

        # Step 5: Delete recipient
        print(f"  Deleting recipient: {recipient_id}")
        delete_response = settings.deleteRecipients(self.token, self.server, recipient_id)
        self.assertIn(delete_response.status_code, [200, 204],
                     f"Failed to delete recipient: {delete_response.status_code} - {delete_response.text}")
        print(f"  Successfully deleted recipient")

        # Step 6: Verify deletion
        time.sleep(2)

        get_response3 = settings.getRecipients(self.token, self.server)
        self.assertEqual(get_response3.status_code, 200)

        recipients3 = get_response3.json()
        recipient_names3 = [r.get('name') for r in recipients3 if isinstance(r, dict)]
        self.assertNotIn(recipient_name, recipient_names3,
                        f"Recipient {recipient_name} still exists after deletion")
        print(f"  Verified recipient was deleted")


if __name__ == '__main__':
    if E2E_ENABLED:
        print("="*80)
        print("UCMDB REST API End-to-End Tests")
        print("="*80)
        print("WARNING: These tests will create and delete resources on UCMDB")
        print("Only run against test/development servers!")
        print("="*80)

    unittest.main(verbosity=2)
