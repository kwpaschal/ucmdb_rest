import pytest
import json
import os
import urllib3
from ucmdb_rest.client import UCMDBServer

# Suppress SSL warnings globally for all tests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@pytest.fixture(scope="session")
def creds():
    """Load credentials from JSON."""
    cred_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
    with open(cred_path, 'r') as f:
        return json.load(f)

@pytest.fixture(scope="session")
def ucmdb_client(creds):
    """Pass the 'creds' fixture into the client fixture."""
    return UCMDBServer(
        user=creds['user'],
        password=creds['password'],
        server=creds['server'],
        port=creds.get('port', 8443),
        ssl_validation=creds.get('ssl_validation', False)
    )