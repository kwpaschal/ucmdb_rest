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
```
## Functional Modules

The library is organized into specialized modules to mirror the UCMDB API ecosystem:

| Module | Description |
| :--- | :--- |
| **client** | `UCMDBServer` class which acts as the entry point. |
| **data_flow_management** | Operations affecting Data Flow Probes. |
| **datamodel** | CRUD operations for Configuration Items (CIs) and Relations. |
| **discovery** | Management of discovery jobs, probe status, and results. |
| **expose_ci** | On-demand queries of the UCMDB database. |
| **integration** | Operations affecting integration points. |
| **ldap** | Operations affecting LDAP integration in UCMDB. |
| **management_zone** | Operations affecting UCMDB UI zone-based discovery. |
| **packages** | Deployment and management of UCMDB Content Packs. |
| **policies** | Policy calculation and automated result chunking. |
| **report** | Operations involving reports and data exports. |
| **settings** | Operations involving infrastructure settings and recipients. |
| **system** | Licensing, versioning, and ping operations. |
| **topology** | TQL execution, ad-hoc queries, and fetching CI attributes. |
| **utils** | Shared helper functions and internal constants. |

## Documentation

For detailed API references, view our [Interactive Documentation](reference/data_flow_management.md).

### Documentation Workflow
The docs are powered by `mkdocs` and `mkdocstrings`.
- **Source**: Python Docstrings (numpy Style)
- **Theme**: Material for MkDocs
- **Customization**: Located in `docs/stylesheets/extra.css`

## Development and Testing

We use `pytest` for functional validation. To run the suite:
```bash
# Run all tests with coverage
pytest --cov=ucmdb_rest

# Preview documentation locally
mkdocs serve

## Release History

## Release History

* **2.0.0 (Current)**
  * **Major Architecture Milestone**: Completed the migration of all legacy `rest.py` components.
  * Re-engineered core modules into a modular, object-oriented framework.
  * Standardized response handling using `requests.Response` objects across all modules.
  * Enhanced code discoverability via the unified `UCMDBServer` entry point.
* **1.7.0**
  * (Internal version alignment release)
* **1.6.0**
  * Added Settings and Recipients management.
* **1.5.0**
  * Added Reports functionality and tests.
* **1.4.0**
  * Added Management Zone functionality and tests.
* **1.3.0**
  * Added LDAP configuration retrieval.
* **1.2.0**
  * Added integration point retrieval.
* **1.1.0**
  * Added ExposeCI ad-hoc query support.
* **1.0.0**
  * Initial stable release: Topology and Discovery modules complete.