import pytest


@pytest.fixture(scope="module")
def active_probe_name(ucmdb_client):
    """Fetches the first available probe name from the server."""
    probes = ucmdb_client.data_flow.getProbeInfo()
    probe_list = probes.json()
    items = probe_list.get('items',[])
    if not items:
        pytest.skip("No probes found on the UCMDB server; skipping dependent tests.")
    return items[0]['probeName']

def test_getProbeRanges(ucmdb_client, active_probe_name):
    # Now you use the dynamic name instead of a hard-coded string
    ranges = ucmdb_client.data_flow.getProbeRanges(active_probe_name)
    assert ranges is not None
    assert isinstance(ranges, list)

def test_addRange(ucmdb_client,active_probe_name):
    RANGE_TO_ADD = [{
        'range': '15.1.1.1-15.1.1.2',
        'definitionType': 'IP_RANGE',
        'ipVersion': 'IPV4',
        'isIncluded': True,
        'rangeType': 'DATA_CENTER',
        'description': 'Test Range'
    }]
    result = ucmdb_client.data_flow.addRange(RANGE_TO_ADD, active_probe_name)
    assert result.status_code == 200

def test_updateRange(ucmdb_client, active_probe_name):
    RANGE_TO_UPDATE = {
            "oldRanges": [{
                "probe": active_probe_name,
                "range": "15.1.1.1-15.1.1.2",
                "definitionType": "IP_RANGE",
                "ipVersion": "IPV4",
                "isIncluded": True
            }],
            "newRanges": [{
                "probe": active_probe_name,
                "range": "15.1.1.1-15.1.1.3",
                "definitionType": "IP_RANGE",
                "ipVersion": "IPV4",
                "isIncluded": True,
                "rangeType": "DATA_CENTER",
                "description": "Updated via Test"
            }]
        }
    result = ucmdb_client.data_flow.updateRange(RANGE_TO_UPDATE, active_probe_name)
    assert result.status_code == 200

def test_deleteRange(ucmdb_client,active_probe_name):
    RANGE_TO_DELETE = [
        {
            "range": "15.1.1.1-15.1.1.3",
            "definitionType": "IP_RANGE",
            "ipVersion": "IPV4",
            "isIncluded": True
        }
    ]
    result = ucmdb_client.data_flow.deleteRange(RANGE_TO_DELETE, active_probe_name)
    assert result.status_code == 200

def test_getAllDomains(ucmdb_client):
    result = ucmdb_client.data_flow.getAllDomains()
    assert result.status_code == 200

def test_getAllCredentials(ucmdb_client):
    result = ucmdb_client.data_flow.getAllCredentials()
    assert result.status_code == 200

def test_getProbeInfo(ucmdb_client):
    result = ucmdb_client.data_flow.getProbeInfo()
    assert result.status_code == 200

def test_getProtocol(ucmdb_client):
    result = ucmdb_client.data_flow.getProtocol('ntadminprotocol')
    assert result.status_code == 200

def test_probeStatusDetails(ucmdb_client,active_probe_name):
    result = ucmdb_client.data_flow.probeStatusDetails('DefaultDomain', active_probe_name)
    assert result.status_code == 200

def test_checkCredential(ucmdb_client,active_probe_name):
    # Adjust "CMS_1_1" to a valid credential ID in your environment if needed
    result = ucmdb_client.data_flow.checkCredential("CMS_1_1", active_probe_name, "10.0.0.1")
    assert result.status_code != 404

def test_getAllProtocols(ucmdb_client):
    result = ucmdb_client.data_flow.getAllProtocols()
    assert result.status_code == 200

def test_getCredentialProfiles(ucmdb_client):
    result = ucmdb_client.data_flow.getCredentialProfiles()
    assert result.status_code == 200

def test_probeStatus(ucmdb_client):
    result = ucmdb_client.data_flow.probeStatus()
    assert result.status_code == 200

def test_queryIPs(ucmdb_client):
    result = ucmdb_client.data_flow.queryIPs('10.1.1.')
    assert result.status_code == 200

def test_queryProbe(ucmdb_client):
    result = ucmdb_client.data_flow.queryProbe()
    assert result.status_code == 200