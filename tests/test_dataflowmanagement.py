import pytest

PROBE_NAME = 'SACUCMRL2305WD'

RANGE_TO_ADD = [{
    'range': '15.1.1.1-15.1.1.2',
    'definitionType': 'IP_RANGE',
    'ipVersion': 'IPV4',
    'isIncluded': True,
    'rangeType': 'DATA_CENTER',
    'description': 'Test Range'
}]

RANGE_TO_UPDATE = {
    "oldRanges": [{
        "probe": PROBE_NAME,
        "range": "15.1.1.1-15.1.1.2",
        "definitionType": "IP_RANGE",
        "ipVersion": "IPV4",
        "isIncluded": True
    }],
    "newRanges": [{
        "probe": PROBE_NAME,
        "range": "15.1.1.1-15.1.1.3",
        "definitionType": "IP_RANGE",
        "ipVersion": "IPV4",
        "isIncluded": True,
        "rangeType": "DATA_CENTER",
        "description": "Updated via Test"
    }]
}

RANGE_TO_DELETE = [
    {
        "range": "15.1.1.1-15.1.1.3",
        "definitionType": "IP_RANGE",
        "ipVersion": "IPV4",
        "isIncluded": True
    }
]

def test_addRange(ucmdb_client):
    result = ucmdb_client.dataflowmanagement.addRange(RANGE_TO_ADD, PROBE_NAME)
    assert result.status_code == 200

def test_updateRange(ucmdb_client):
    result = ucmdb_client.dataflowmanagement.updateRange(RANGE_TO_UPDATE, PROBE_NAME)
    assert result.status_code == 200

def test_deleteRange(ucmdb_client):
    # Using the range from the update for a clean teardown
    result = ucmdb_client.dataflowmanagement.deleteRange(RANGE_TO_DELETE, PROBE_NAME)
    assert result.status_code == 200

def test_getAllDomains(ucmdb_client):
    result = ucmdb_client.dataflowmanagement.getAllDomains()
    assert result.status_code == 200

def test_getAllCredentials(ucmdb_client):
    result = ucmdb_client.dataflowmanagement.getAllCredentials()
    assert result.status_code == 200

def test_getProbeInfo(ucmdb_client):
    result = ucmdb_client.dataflowmanagement.getProbeInfo()
    assert result.status_code == 200

def test_getProbeRanges(ucmdb_client):
    result = ucmdb_client.dataflowmanagement.getProbeRanges(PROBE_NAME)
    assert result.status_code == 200

def test_getProtocol(ucmdb_client):
    result = ucmdb_client.dataflowmanagement.getProtocol('ntadminprotocol')
    assert result.status_code == 200

def test_probeStatusDetails(ucmdb_client):
    result = ucmdb_client.dataflowmanagement.probeStatusDetails('DefaultDomain', PROBE_NAME)
    assert result.status_code == 200

def test_checkCredential(ucmdb_client):
    # Adjust "CMS_1_1" to a valid credential ID in your environment if needed
    result = ucmdb_client.dataflowmanagement.checkCredential("CMS_1_1", PROBE_NAME, "10.0.0.1")
    assert result.status_code != 404