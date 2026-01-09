import pytest


def test_system_ping(ucmdb_client):
    # This must start with test_
    response = ucmdb_client.system.ping()
    # If ping returns a Response object, we check status_code
    # If it returns a dict, we'd check the keys.
    assert response.status_code == 200

def test_system_version(ucmdb_client):
    response = ucmdb_client.system.getUCMDBVersion()
    assert response.status_code == 200

def test_system_license(ucmdb_client):
    response = ucmdb_client.system.getLicenseReport()
    assert response.status_code == 200