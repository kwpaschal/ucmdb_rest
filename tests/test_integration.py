import pytest


def test_integration_list_and_details(ucmdb_client):
    """Verify listing all IPs and then fetching details for each (Command 59 logic)."""
    info_res = ucmdb_client.integrations.getIntegrationInfo()
    assert info_res.status_code == 200
    json_results = info_res.json()
    assert isinstance(json_results, dict)

    if json_results:
        for ipoint_name in json_results:
            details = ucmdb_client.integrations.getIntegrationDetails(ipoint_name, detail='false')
            assert details.status_code == 200
            assert details.json()["name"] == ipoint_name
            break 
    else:
        pytest.skip("No integration points found to test.")

def test_clear_cache(ucmdb_client):
    ipoints = ucmdb_client.integrations.getIntegrationInfo().json()
    
    # Define system integrations to skip
    system_points = {'HistoryDataSource', 'UCMDBDiscovery'}
    integration_point = ''
    job_name = ''
    dict_to_clear = {}

    for name, info in ipoints.items():
        if name in system_points:
            continue
            
        # Check both Population and Push jobs
        jobs = info.get('dataPopulationJobs', []) + info.get('dataPushJobs', [])
        
        if jobs:
            # We found a target! Let's take the first job's displayID
            job_name = jobs[0]['displayID']
            integration_point = name
            dict_to_clear = {name: [job_name]}
            break # Exit the loop once we have a target for the test

    # Ensure we actually found something before calling clear_cache
    assert dict_to_clear, "No valid integration jobs found to test cache clearing."
    
    clear = ucmdb_client.integrations.clear_cache(dict_to_clear)
    assert clear.status_code == 200
    # Now call activate function
    activate = ucmdb_client.integrations.setEnabledState(integration_point,True)
    assert activate.status_code == 200
    # Now run a delta sync
    sync = ucmdb_client.integrations.syncIntegrationPointJob(integration_point,
                                                             job_name,
                                                             'population_delta')
    assert sync.status_code == 200
    