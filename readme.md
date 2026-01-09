# UCMDB REST Python Library

A modern, object-oriented Python 3.6+ wrapper for the OpenText Universal Configuration Management Database (UCMDB) REST API. This library centralizes UCMDB interactions through a unified client, providing type-safe Enums and automated pagination.

## Quick Start

The library uses a central `UCMDBServer` to manage authentication and session persistence. 

```python
from ucmdb_rest import UCMDBServer
from ucmdb_rest.policies import ComplianceStatus

# Initialize connection
client = UCMDBServer(
    server="ucmdb.example.com", 
    user="admin", 
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
# Run all tests with coverage
pytest --cov=ucmdb_rest

# Lint the code
ruff check .

# Preview documentation
mkdocs serve
```
## Additional Documentation

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