# UCMDB REST Python Library

A modern, object-oriented Python 3.6+ wrapper for the OpenText Universal Configuration Management Database (UCMDB) REST API. This library centralizes UCMDB interactions through a unified client, providing type-safe Enums and automated pagination.
## Setup and Authentication
This library contains some examples that assume a `credentials.json` file is in the same direcory as the code.

1. Copy `credentials.json.example` to `credentials.json`
2. Update the values with your UCMDB server details

| Key | Description |
| :--- | :--- |
| **user** | UCMDB Username |
| **password** | UCMDB Password |
| **server** | FQDN or IP of the UCMDB Server |
| **port** | REST API port (Default 8443) |
| **ssl_validation** | Boolean (false to skip certificate checks) |

## Quick Start

The library uses a central `UCMDBServer` to manage authentication and session persistence. 

```python
from ucmdb_rest import UCMDBServer

# Initialize client (assumes credentials.json exists)
client = UCMDBServer.from_json('credentials.json')

# Quick connectivity check
print(f"Connected to: {client.server_version}")

# Get detailed version info
version = client.system.getUCMDBVersion().json()
print(f"Product: {version['productName']}")
print(f"Content Pack: {version['contentPackVersion']}")
```
## Practical Examples
To help you get started quickly, here are some example standalone scripts
* **`add_cis.py`**: Create CIs and Relationships with custom properties
* **`delete_cis.py`**: Delete CIs by their UCMDB ID
* **`get_recon_rule.py`**: Display a reconciliation rule for a CI Type
* **`initialize_get_version.py`**: Display version information about the UCMDB Server
* **`query_topology`**: Run a UCMDB View and get the information
* **`search_and_expose_ci.py`**: Search for a CI by name and get specific properties
* **`show_content_packs.py`**: Display current content pack information
* **`show_license_report.py`**: Display a license report from UCMDB

see [Examplese Documentation](./Examples/README.md) for detailed setup and usage.
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
* **2.0.1 (Current)**
  * Fixed a bunch of failing tests
  * Beginning to add Examples
* **2.0.0**
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