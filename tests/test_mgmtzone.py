import pytest
import time

def test_management_zone_full_lifecycle(ucmdb_client):
    # Setup unique names to avoid collisions
    timestamp = int(time.time())
    profile_name = f"Test_Profile_{timestamp}"
    zone_name = f"Test_Zone_{timestamp}"

    # 1. Create the Job Group (Discovery Profile)
    job_group_payload = {
        "name": profile_name,
        "description": "Temporary profile for REST API testing",
        "jobs": [
            {
                "jobName": "Range IPs by ICMP",
                "jobDisplayName": "Range IPs by ICMP",
                "adapterName": "ICMP_NET_Dis_IpRange",
                "inputCI": "discoveryprobegateway",
                "jobType": "DynamicService",
                "jobInvokeOnNewTrigger": True
            }
        ]
    }

    try:
        print(f"\n[1/4] Creating Job Group: {profile_name}")
        jg_res = ucmdb_client.discovery.createJobGroup(job_group_payload)
        assert jg_res.status_code == 200, f"Failed to create Job Group: {jg_res.text}"

        # 2. Create the Management Zone
        mz_payload = {
            "name": zone_name,
            "activated": False,
            "ipRangeProfiles": [{"ipRangeProfileId": "All IP Range Groups"}],
            "discoveryActivities": [
                {
                    "discoveryProfileId": profile_name,
                    "scheduleProfileId": "Interval 1 Day (Default)",
                    "credentialProfileId": "All Credentials"
                }
            ]
        }

        print(f"[2/4] Creating Management Zone: {zone_name}")
        mz_res = ucmdb_client.mgmt_zones.createManagementZone(mz_payload)
        assert mz_res.status_code == 200, f"Failed to create Management Zone: {mz_res.text}"

    finally:
        # 3. Delete the Management Zone
        print(f"[3/4] Deleting Management Zone: {zone_name}")
        ucmdb_client.mgmt_zones.deleteManagementZone(zone_name)

        # 4. Delete the Job Group
        print(f"[4/4] Deleting Job Group: {profile_name}")
        ucmdb_client.discovery.deleteSpecificJobGroup(profile_name)
        
        print("Cleanup complete. No artifacts remain.")

def test_getMgmtZone(ucmdb_client):
    result = ucmdb_client.mgmt_zones.getMgmtZone()
    assert result.status_code==200

def test_getSpecificMgmtZoneandStatistics(ucmdb_client):
    result = ucmdb_client.mgmt_zones.getMgmtZone()
    items = result.json()
    if len(items["items"]) > 0:
        zone_to_test = items["items"][0]["name"]
        newresult = ucmdb_client.mgmt_zones.getSpecificMgmtZone(zone_to_test)
        assert newresult.status_code == 200
        statsresult = ucmdb_client.mgmt_zones.getStatisticsForZone(zone_to_test)
        assert statsresult.status_code == 200