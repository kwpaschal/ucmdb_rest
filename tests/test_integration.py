"""
Integration tests for ucmdb_rest library

Tests actual function calls with version checking against real or mocked UCMDB servers.
Can run in two modes:
- Mock mode: Uses mocked responses (default)
- Live mode: Uses real UCMDB servers (requires credentials.json)
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ucmdb_rest import (
    createHeaders,
    getUCMDBVersion,
    UCMDBVersionError,
    clear_version_cache
)

# Import modules to test
from ucmdb_rest import utils
from ucmdb_rest import packages
from ucmdb_rest import datamodel
from ucmdb_rest import topology
from ucmdb_rest import policies
from ucmdb_rest import discovery
from ucmdb_rest import dataflowmanagment
from ucmdb_rest import mgmtzone
from ucmdb_rest import settings
from ucmdb_rest import integration
from ucmdb_rest import ldap


# Check if we should run live tests
LIVE_MODE = os.environ.get('UCMDB_TEST_LIVE', 'false').lower() == 'true'
CREDENTIALS_FILE = os.path.join(
    os.path.dirname(__file__),
    '..',
    'ucmdb_rest',
    'discovery',
    'credentials.json'
)


def load_test_credentials():
    """Load test server credentials if available"""
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            config = json.load(f)
            return config.get('servers', [])[0] if config.get('servers') else None
    return None


class TestAuthenticationWithVersionChecking(unittest.TestCase):
    """Test authentication and version retrieval"""

    def setUp(self):
        """Clear version cache before each test"""
        clear_version_cache()

    @unittest.skipUnless(LIVE_MODE, "Skipping live test (set UCMDB_TEST_LIVE=true to enable)")
    def test_live_authentication(self):
        """Test real authentication to UCMDB server"""
        server = load_test_credentials()
        if not server:
            self.skipTest("No credentials available")

        token = createHeaders(
            server['username'],
            server['password'],
            server['hostname'],
            port=server['port']
        )

        self.assertIsInstance(token, dict)
        self.assertIn('Authorization', token)

    @unittest.skipUnless(LIVE_MODE, "Skipping live test")
    def test_live_version_retrieval(self):
        """Test retrieving version from real UCMDB server"""
        server = load_test_credentials()
        if not server:
            self.skipTest("No credentials available")

        token = createHeaders(
            server['username'],
            server['password'],
            server['hostname'],
            port=server['port']
        )

        response = getUCMDBVersion(token, server['hostname'])
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('contentPackVersion', data)
        self.assertIn('fullServerVersion', data)


class TestFunctionsWithMockedVersions(unittest.TestCase):
    """Test that functions properly check versions using mocked responses"""

    def setUp(self):
        """Setup mocks before each test"""
        clear_version_cache()
        self.mock_token = {"Authorization": "Bearer test"}
        self.mock_server = "test-server.example.com"

    def _mock_ucmdb_response(self, version, status_code=200, response_data=None):
        """Helper to mock UCMDB responses"""
        def mock_request(*args, **kwargs):
            response = Mock()
            response.status_code = status_code
            if response_data:
                response.json.return_value = response_data
            return response

        # Mock version check
        version_patch = patch('ucmdb_rest.utils.getUCMDBVersion')
        mock_version = version_patch.start()
        version_response = Mock()
        version_response.status_code = 200
        version_response.json.return_value = {
            "fullServerVersion": "11.8.0",
            "contentPackVersion": version
        }
        mock_version.return_value = version_response

        # Mock actual API call
        request_patch = patch('requests.get', side_effect=mock_request)
        mock_request_obj = request_patch.start()

        self.addCleanup(version_patch.stop)
        self.addCleanup(request_patch.stop)

        return mock_version, mock_request_obj

    def test_function_with_compatible_version(self):
        """Test that functions work with compatible UCMDB version"""
        self._mock_ucmdb_response(
            "25.4",
            200,
            {"data": "test"}
        )

        # This should work - 25.4 >= 2023.05
        response = utils.getLicenseReport(self.mock_token, self.mock_server)
        self.assertEqual(response.status_code, 200)

    def test_function_blocks_incompatible_version(self):
        """Test that functions block execution with incompatible version"""
        # Note: We'd need to apply decorators first to test this
        # For now, this test documents the expected behavior
        pass


class TestEndToEndWorkflow(unittest.TestCase):
    """Test complete workflows from authentication to data retrieval"""

    def setUp(self):
        """Setup for end-to-end tests"""
        clear_version_cache()

    @unittest.skipUnless(LIVE_MODE, "Skipping live test")
    def test_complete_workflow_live(self):
        """Test complete workflow: auth -> version check -> API call"""
        server = load_test_credentials()
        if not server:
            self.skipTest("No credentials available")

        # Step 1: Authenticate
        token = createHeaders(
            server['username'],
            server['password'],
            server['hostname'],
            port=server['port']
        )
        self.assertIsInstance(token, dict)

        # Step 2: Check version
        version_response = getUCMDBVersion(token, server['hostname'])
        self.assertEqual(version_response.status_code, 200)
        version_data = version_response.json()

        # Step 3: Make API call
        license_response = utils.getLicenseReport(token, server['hostname'])
        self.assertEqual(license_response.status_code, 200)

    def test_complete_workflow_mocked(self):
        """Test complete workflow with mocked responses"""
        mock_token = {"Authorization": "Bearer test"}
        mock_server = "test-server"

        with patch('ucmdb_rest.utils.authenticate') as mock_auth, \
             patch('ucmdb_rest.utils.getUCMDBVersion') as mock_version, \
             patch('requests.get') as mock_get:

            # Setup mocks
            auth_response = Mock()
            auth_response.status_code = 200
            auth_response.json.return_value = {"token": "test-token"}
            mock_auth.return_value = auth_response

            version_response = Mock()
            version_response.status_code = 200
            version_response.json.return_value = {
                "contentPackVersion": "25.4",
                "fullServerVersion": "11.8.0"
            }
            mock_version.return_value = version_response

            api_response = Mock()
            api_response.status_code = 200
            api_response.json.return_value = {"data": "test"}
            mock_get.return_value = api_response

            # Execute workflow
            token = createHeaders("admin", "password", mock_server)
            version = getUCMDBVersion(token, mock_server)
            response = utils.getLicenseReport(token, mock_server)

            # Verify
            self.assertEqual(version.status_code, 200)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    # Run tests
    if LIVE_MODE:
        print("Running in LIVE mode - will test against real UCMDB server")
    else:
        print("Running in MOCK mode - set UCMDB_TEST_LIVE=true for live tests")

    unittest.main()
