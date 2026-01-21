# -*- coding: utf-8 -*-
import time

import pytest

# Constants for the test environment
TARGET_VIEW = "All My Windows Servers"

@pytest.fixture
def time_range():
    now_ms = int(time.time() * 1000)
    three_days_ago_ms = now_ms - (3*24*60*60*1000)
    return three_days_ago_ms, now_ms

def test_change_reports_all_windows(ucmdb_client, time_range):
    ci_name = f"Test_Win_Node_{int(time.time())}"
    myCI = {
            "cis": [
                    {
                    "ucmdbId": "1",
                    "type": "nt",
                    "properties": {"name":ci_name,
                                    "os_family":"windows"}
                    }
                ],
                "relations": []
            }
    create_res = ucmdb_client.data_model.addCIs(myCI, returnIdsMap=True)
    data = create_res.json()
    ci_id = data.get('idsMap',{}).get("1")
    try:
        update_ci = {
                        "type": "nt",
                        "properties": {
                            "name": ci_name,
                            "os_family": "windows",
                            "data_note": "Modified for test report"
                        }
                    }
        ucmdb_client.data_model.updateCI(ci_id, update_ci)
        time.sleep(3)
        from_time, to_time = time_range


        response = ucmdb_client.reports.changeReportsAll(view="All My Windows Servers",
                                                         toTime=to_time,
                                                         fromTime=from_time)
        
        result = response.json()
        items = result.get('items',{})
        found = ci_id in items
        if not found:
            print(f"IDs found in report: {list(items.keys())}")
        assert response.status_code == 200

    finally:
        ucmdb_client.data_model.deleteCIs(ci_id)

def test_change_reports_blacklist_windows(ucmdb_client, time_range):
    from_time, to_time = time_range
    response = ucmdb_client.reports.changeReportsBlacklist(to_time, from_time, TARGET_VIEW)
    
    assert response.status_code == 200
    res_json = response.json()
    
    # Check that we got a dictionary back
    assert isinstance(res_json, dict)
    
    # If the view had changes, verify the structure of the first item
    if len(res_json) > 0:
        first_id = list(res_json.keys())[0]
        assert 'changesMap' in res_json[first_id]
        assert 'ciID' in res_json[first_id]
        print(f"Verified change for CI: {res_json[first_id]['displayLabel']}")

def test_change_reports_whitelist_windows(ucmdb_client, time_range):
    from_time, to_time = time_range
    
    response = ucmdb_client.reports.changeReportsWhitelist(to_time, from_time, TARGET_VIEW)
    assert response.status_code == 200
    res_json = response.json()
    assert isinstance(res_json, dict)