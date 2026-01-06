import pytest

def test_integration_list_and_details(ucmdb_client):
    """Verify listing all IPs and then fetching details for each (Command 59 logic)."""
    info_res = ucmdb_client.integration.getIntegrationInfo()
    assert info_res.status_code == 200
    json_results = info_res.json()
    assert isinstance(json_results, dict)

    if json_results:
        for ipoint_name in json_results:
            details = ucmdb_client.integration.getIntegrationDetails(ipoint_name, detail='false')
            assert details.status_code == 200
            assert details.json()["name"] == ipoint_name
            break 
    else:
        pytest.skip("No integration points found to test.")