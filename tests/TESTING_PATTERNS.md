# Testing Patterns from Real-World Usage

This document summarizes testing patterns extracted from Keith's comprehensive REST API testing script (`OLD_rest_libs/rest.py` - 2167 lines, 97 different test scenarios).

## Key Insights

### 1. Interactive Menu-Driven Testing
The original test script uses an interactive menu system with 97 different test scenarios covering all UCMDB REST API endpoints. This approach allows:
- Manual testing of specific functionality
- Real-time feedback and validation
- Flexible parameter input for different test cases
- Easy verification of API behavior

### 2. Setup/Teardown Pattern for State-Dependent Operations

#### Pattern: Verify Before Delete
```python
# Example from command 45 (delete job group)
job_group = input('Enter the name of the Job Group to DELETE: ')

# Verify it exists first
getjobs = runMethod(getJobGroup, headers, ucmdb_server)
j = getjobs.json()
existing_jobs = []
for key in j:
    for index in range(len(j[key])):
        for akey in j[key][index]:
            if akey == 'id':
                existing_jobs.append(j[key][index][akey])

# Only delete if it exists
if job_group in existing_jobs:
    print('Deleting job group:', job_group)
    jobs = deleteSpecificJobGroup(headers, ucmdb_server, job_group)
    print('Ran deleteSpecificJobGroup with a status of:', jobs.status_code)
    print('The job is GONE')
else:
    print('The job group name you entered is INVALID.')
    print('Please rerun this script with item 41 to list the valid jobs')
```

**Key Principle**: Always verify the resource exists before attempting to delete it.

#### Pattern: Create with Unique Identifiers
```python
# Example from command 68 (bulk CI creation)
ci_name = input('Enter the name node to use as a base: ')
number_to_insert = input('Enter the number of CIs to create: ')

ci_list = []
for i in range(int(number_to_insert)):
    myname = str(ci_name) + str(i)  # Unique name: node0, node1, node2...
    myname_fqdn = str(ci_name) + str(i) + "." + str(domainName)
    ci_list.append({
        "ucmdbId": i,
        "type": "node",
        "properties": {"name": myname, "primary_dns_name": myname_fqdn}
    })
```

**Key Principle**: Use sequential numbering or UUIDs for test data to avoid naming conflicts.

#### Pattern: Create with UUIDs for Relations
```python
# Example from command 69 (bulk CIs with relations)
for i in range(int(number_to_insert)):
    myuuid = str(uuid.uuid4())        # Unique CI ID
    agent_id = str(uuid.uuid4())      # Unique agent ID
    relation_id = str(uuid.uuid4())   # Unique relation ID

    ci_list.append({
        "ucmdbId": myuuid,
        "type": "node",
        "properties": {"name": myname, "primary_dns_name": myname_fqdn}
    })
    ci_list.append({
        "ucmdbId": agent_id,
        "type": "hp_operations_agent",
        "properties": {"name": agent_id, "discovered_product_name": "hp_operations_agent"}
    })
    relations_list.append({
        "ucmdbId": relation_id,
        "type": "composition",
        "end1Id": myuuid,
        "end2Id": agent_id,
        "properties": {}
    })
```

**Key Principle**: Use UUIDs for complex objects with relationships to ensure uniqueness.

### 3. Common Test Workflows

#### Workflow 1: Create → Verify → Delete
1. **Create**: Deploy test resource (CI, job group, package, etc.)
2. **Verify**: Query to confirm resource was created successfully
3. **Delete**: Remove test resource to clean up

#### Workflow 2: Get All → Get Specific → Modify
1. **Get All**: Retrieve list of resources (e.g., all job groups)
2. **Get Specific**: Retrieve details of one resource
3. **Modify**: Update or delete the specific resource

#### Workflow 3: Bulk Operations
1. **Create Many**: Insert large number of CIs (1000+) for performance testing
2. **Query Results**: Verify all CIs were created
3. **Clean Up**: Delete all test CIs

### 4. Test Data Patterns

#### Naming Conventions
- Base name + sequence number: `node0`, `node1`, `node2`
- Base name + domain: `node0.mycompany.com`
- UUID-based names for guaranteed uniqueness: `str(uuid.uuid4())`

#### Common Test Objects

**Simple CI (Node)**:
```python
{
    "ucmdbId": i,
    "type": "node",
    "properties": {"name": "testnode1", "primary_dns_name": "testnode1.mycompany.com"}
}
```

**CI with Relations (Node + Agent)**:
```python
{
    "cis": [
        {
            "ucmdbId": node_id,
            "type": "node",
            "properties": {"name": "testnode1"}
        },
        {
            "ucmdbId": agent_id,
            "type": "hp_operations_agent",
            "properties": {"name": agent_id, "discovered_product_name": "hp_operations_agent"}
        }
    ],
    "relations": [
        {
            "ucmdbId": relation_id,
            "type": "composition",
            "end1Id": node_id,
            "end2Id": agent_id,
            "properties": {}
        }
    ]
}
```

**Job Group**:
```python
{
    "name": "Test_Job_Group",
    "type": "CMS",
    "oob": False,
    "description": "Test job group created by automated test",
    "discoveryType": None,
    "jobs": [
        {
            "jobName": "Inventory Discovery by Scanner",
            "jobDisplayName": "Inventory Discovery by Scanner",
            "adapterName": "InventoryDiscoveryByScanner",
            "inputCI": "node",
            "jobType": "WorkflowService",
            "protocols": ["ntadminprotocol", "sshprotocol"],
            "jobParameters": {},
            "triggerQueries": [],
            "jobInvokeOnNewTrigger": True
        }
    ]
}
```

### 5. Error Handling Patterns

#### Pattern: Check Before Action
```python
# Don't assume resource exists - verify first
if job_group in existing_jobs:
    # Perform action
else:
    print('Resource not found - aborting')
```

#### Pattern: Validate Input
```python
ci_to_remove = input('Enter the ID to remove: ')
if ci_to_remove == '':
    print('No value entered. Exiting.')
    sys.exit(command)
```

#### Pattern: Provide Helpful Feedback
```python
print('Deleting job group:', job_group)
jobs = deleteSpecificJobGroup(headers, ucmdb_server, job_group)
print('Ran deleteSpecificJobGroup with a status of:', jobs.status_code)
print('The job is GONE')
```

### 6. Test Categories (97 Total Scenarios)

From the menu system, test scenarios cover:

**CI Operations (15 scenarios)**:
- Add CI (single and bulk)
- Delete CI
- Update CI
- Expose CI
- Query CIs

**Discovery Operations (10 scenarios)**:
- Job groups (create, delete, list, get specific)
- IP ranges
- Schedules
- Module tree
- Use cases
- Job metadata

**Package Management (8 scenarios)**:
- Deploy package
- Delete package
- Get packages
- Content packs
- Progress tracking

**Credentials & Probes (12 scenarios)**:
- Create credentials
- Manage ranges
- Probe operations
- Check credentials
- Query IPs

**Management Zones (5 scenarios)**:
- List zones
- Get specific zone
- Create zone
- Delete zone
- Activate zone

**Policies & Compliance (5 scenarios)**:
- Get policies
- Get compliance views
- Calculate compliance
- Get non-compliant CIs

**Integration & Settings (8 scenarios)**:
- Integration points
- Recipients
- LDAP settings
- Settings management

**Reporting (3 scenarios)**:
- Change reports (all attributes, blacklist, whitelist)

**Recon Analyzer (3 scenarios)**:
- Get CI by name
- View operations
- Match reasons

**Other (28 scenarios)**:
- Views, queries, license reports, version info, etc.

## Recommendations for Automated Tests

### For Unit Tests (Fast, Always Run)
- Mock all HTTP calls
- Test version checking logic
- Test parameter validation
- Test error handling

### For Integration Tests (Medium, Run on Commit)
- Mock UCMDB responses
- Test workflow logic (create → verify → delete)
- Test edge cases
- Verify correct API calls are made

### For End-to-End Tests (Slow, Run Before Release)
- Run against real "crash and burn" UCMDB servers
- Create test resources with unique identifiers (UUID-based names)
- Always clean up (delete test resources)
- Test complete workflows:
  1. Create test CI with unique name
  2. Query to verify it exists
  3. Update the CI
  4. Query to verify update
  5. Delete the CI
  6. Query to verify deletion

### Test Isolation Strategy
- Use timestamp or UUID in test resource names: `test_ci_20231219_145302` or `test_ci_<uuid>`
- Run cleanup before AND after tests (in case previous test failed)
- Never test against production data
- Use dedicated test UCMDB servers for E2E tests

### Test Data Cleanup
```python
def setUp(self):
    """Create test resources with unique identifiers"""
    self.test_id = str(uuid.uuid4())
    self.test_ci_name = f"test_node_{self.test_id}"
    self.created_resources = []  # Track what we create

def tearDown(self):
    """Always clean up test resources, even if test fails"""
    for resource in self.created_resources:
        try:
            # Delete the resource
            delete_function(token, server, resource['id'])
        except:
            pass  # Best effort cleanup - don't fail if already deleted
```

## Key Takeaways

1. **Always verify before delete** - Check resource exists to avoid errors
2. **Use unique identifiers** - UUIDs or timestamps prevent test conflicts
3. **Clean up test data** - Delete created resources in tearDown
4. **Test complete workflows** - Create → Verify → Update → Verify → Delete
5. **Separate test types** - Unit (mocked, fast) vs E2E (live, slow)
6. **Use dedicated test servers** - Never test against production
7. **Handle failures gracefully** - Best-effort cleanup, helpful error messages
8. **Track created resources** - Maintain list for cleanup

## Next Steps

1. Review this document against actual test needs
2. Identify which workflows are critical for automated testing
3. Create E2E test suite based on these patterns
4. Set up test data fixtures for common scenarios
5. Document test server requirements and setup
