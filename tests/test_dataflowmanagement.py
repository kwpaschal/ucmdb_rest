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
    ranges = ucmdb_client.data_flow.getProbeRanges(active_probe_name)
    assert ranges.status_code == 200

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

def test_checkCredential_ad_hoc(ucmdb_client, active_probe_name):
    query_body = {
        "nodes": [
            {
                "type": "ntcmd",
                "queryIdentifier": "ntcmd",
                "visible": True,
                "includeSubtypes": True,
                "layout": ["display_label", "application_ip", "last_discovered_by_probe", "credentials_id"],  # noqa: E501
                "attributesConditions": [ 
                    {
                        "attributeName": "last_discovered_by_probe",
                        "operator": "equals", 
                        "value": active_probe_name
                    }
                ]
            }
        ],
        "relations": []
    }

    response = ucmdb_client.topology.queryCIs(query_body)
    all_cis = response.json().get("cis", [])
    
    matching_cis = [
        ci for ci in all_cis 
        if ci.get("properties", {}).get("last_discovered_by_probe") == active_probe_name
    ]

    assert len(matching_cis) > 0, (
        f"Filtered out all {len(all_cis)} CIs because none matched probe: {active_probe_name}"
    )

    target_ci = matching_cis[0]
    props = target_ci.get("properties", {})
    
    cred_id = props.get("credentials_id")
    ip_addr = props.get("application_ip")
    probe_name = props.get("last_discovered_by_probe")

    print(f"Found {len(matching_cis)} matches. Testing Credential: {cred_id} on {ip_addr}")

    result = ucmdb_client.data_flow.checkCredential(cred_id, probe_name, ip_addr)
    
    assert result.status_code == 200
    print(f"Successfully validated credential for {ip_addr} via {probe_name}")

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