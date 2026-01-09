import pytest
from ucmdb_rest.client import UCMDBAuthError, UCMDBServer


def test_connection_and_auth(ucmdb_client):
    """
    This test verifies that the fixture in conftest.py successfully 
    authenticated and returned a working client object.
    """
    # Verify the base URL was built
    assert ucmdb_client.base_url.startswith("https://")
    
    # Verify the token is present in the session headers
    auth_header = ucmdb_client.session.headers.get('Authorization')
    assert auth_header is not None
    assert auth_header.startswith("Bearer ")
    
    # Optional: Verify the token isn't just an empty string
    assert len(auth_header) > 20

def test_failed_connection_bad_server():
    with pytest.raises(ConnectionError) as excinfo:
        UCMDBServer(
            user="admin",
            password="ucmdbadmin",
            server="bad.server.local"
        )
    assert "Failed to resolve" in str(excinfo.value)

# def test_failed_auth_bad_password(creds): 
#     with pytest.raises(UCMDBAuthError) as excinfo:
#         UCMDBServer(
#             user=creds['user'],
#             password="wrong_password",
#             server=creds['server']
#         )
#    
#    error_msg = str(excinfo.value)
#    assert "Auth Failed" in error_msg
#    assert "401" in error_msg