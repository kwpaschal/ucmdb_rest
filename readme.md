# UCMDB REST Python Library

A modern, object-oriented Python 3.6+ wrapper for the OpenText Universal Configuration Management Database (UCMDB) REST API. This library centralizes UCMDB interactions through a unified client, providing type-safe Enums and automated pagination.

## Quick Start

The library uses a central `UCMDBClient` to manage authentication and session persistence. All sub-modules are accessible as attributes of the client.

```python
from ucmdb_rest.client import UCMDBClient
from ucmdb_rest.policies import ComplianceStatus

# Initialize connection
client = UCMDBClient(
    base_url="[https://ucmdb.example.com:8443/rest-api](https://ucmdb.example.com:8443/rest-api)", 
    username="admin", 
    password="password"
)

# Run a Policy Audit with automatic chunking
view_name = "Node Compliance View"
results = client.policies.getAllResultsForPath(
    view_name, 
    status_type=ComplianceStatus.NON_COMPLIANT
)

print(f"Retrieved {len(results)} non-compliant CIs.")

## Functional Modules

The library is organized into specialized modules to mirror the UCMDB API ecosystem:

| Module | Description |
| :--- | :--- |
| **datamodel** | CRUD operations for Configuration Items (CIs) and Relations. |
| **policies** | Policy calculation, compliance views, and automated result chunking. |
| **topology** | TQL execution, ad-hoc queries, and fetching CI attributes. |
| **discovery** | Management of discovery jobs, probe status, and results. |
| **packages** | Deployment and management of UCMDB Content Packs. |
| **utils** | Shared helper functions, including URL encoding via `urllib.parse.quote`. |

## Development and Testing

We use `pytest` for functional validation. To run the suite:

```bash
# Run all tests
pytest

# Run a specific test with stdout enabled
pytest -s tests/test_policies.py

# Run a specific test with stdout enabled
pytest -s tests/test_policies.py

## Additional Documentation

Detailed guides and historical context can be found in the `docs/` directory:
* **IMPLEMENTATION_SUMMARY.md**: Historical technical overview of the API integration.
* **TODO.md**: Active roadmap and upcoming feature tracking.

## Release History

* **1.2.0 (Current)**
  * Major refactor to Object-Oriented architecture.
  * Added `ComplianceStatus` Enum for type-safety.
  * Implemented `getAllResultsForPath` automated pagination logic.
* **1.1.0**
  * Standardized docstrings to return `requests.Response` objects.
* **1.0.0**
  * Initial library release.

## Verification

* **MIT License**: Included in `setup.py`.
* **Dependencies**: `requests~=2.31.0` in `install_requires`.
* **Clean Root**: Legacy `.md` files moved to `/docs`.