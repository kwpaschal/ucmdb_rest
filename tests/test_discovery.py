import pytest

# 1. Metadata Tests
def test_get_module_tree(ucmdb_client):
    response = ucmdb_client.discovery.getModuleTree()
    assert response.status_code == 200
    assert "children" in response.json()

def test_get_use_cases(ucmdb_client):
    response = ucmdb_client.discovery.getUseCase()
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "children" in data

def test_get_job_metadata(ucmdb_client):
    response = ucmdb_client.discovery.getJobMetaData()
    assert response.status_code == 200
    assert "items" in response.json()

# 2. IP Range Tests
def test_get_ip_ranges(ucmdb_client):
    response = ucmdb_client.discovery.getIPRange()
    assert response.status_code == 200
    assert "items" in response.json()

def test_get_ip_range_for_specific_ip(ucmdb_client):
    # Testing with a common loopback or local IP
    response = ucmdb_client.discovery.getIPRangeForIP("127.0.0.1")
    assert response.status_code == 200

# 3. Job Group & Parameter Tests
def test_get_job_group_with_fields(ucmdb_client):
    # This specifically tests the fix you just made
    response = ucmdb_client.discovery.getJobGroup(fields="name,id")
    assert response.status_code == 200
    data = response.json()
    if data.get("items"):
        assert "name" in data["items"][0]
        assert "id" in data["items"][0]

def test_get_questions(ucmdb_client):
    job_name = "Host Connection by Shell"
    response = ucmdb_client.discovery.getQuestions(job_name)
    assert response.status_code == 200

def test_get_schedules(ucmdb_client):
    response = ucmdb_client.discovery.getSchedules()
    assert response.status_code == 200

# 4. Lifecycle Test
def test_job_group_lifecycle(ucmdb_client):
    name = "Pytest_Discovery_Test"
    payload = {
        "name": name,
        "type": "CMS",
        "description": "Test Group",
        # discoveryType often defaults to null on the server
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
    # Create
    assert ucmdb_client.discovery.createJobGroup(payload).status_code in [200, 201]
    # Get Specific
    assert ucmdb_client.discovery.getSpecificJobGroup(name).status_code == 200
    # Delete
    assert ucmdb_client.discovery.deleteSpecificJobGroup(name).status_code == 200