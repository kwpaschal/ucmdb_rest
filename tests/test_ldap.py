import pytest

def test_get_ldap_settings(ucmdb_client):
    """Verify we can retrieve LDAP configuration."""
    response = ucmdb_client.ldap.getLDAPSettings()
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    
    if len(data) > 0:
        # Check for key structure elements from your docstring
        assert "connection" in data[0]
        assert "user" in data[0]
        assert "url" in data[0]["connection"]