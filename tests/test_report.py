# -*- coding: utf-8 -*-
import pytest
import time

# Constants for the test environment
TARGET_VIEW = "All My Windows Servers"

@pytest.fixture
def time_range():
    """Generates a 24-hour epoch time range in milliseconds."""
    to_time = int(time.time() * 1000)
    from_time = to_time - (24 * 60 * 60 * 1000 * 7)
    return from_time, to_time

def test_change_reports_all_windows(ucmdb_client, time_range):
    """Verifies retrieval of all changes for the Windows Servers view."""
    from_time, to_time = time_range
    
    # We pass custom attributes to verify the URL string joining logic
    attrs = ['name', 'description']
    
    response = ucmdb_client.reports.changeReportsAll(
        toTime=to_time, 
        fromTime=from_time, 
        view=TARGET_VIEW,
        attributes=attrs
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # UCMDB 'results' endpoint usually returns a list or dict of changes
    assert 'items' in data or 'results' in data or isinstance(data, list)
    print(f"\n--- Global Changes: {TARGET_VIEW} ---")
    print(f"Status: {response.status_code}")

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