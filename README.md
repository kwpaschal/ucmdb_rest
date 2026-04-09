# UCMDB REST Python Library

[![PyPI version](https://badge.fury.io/py/ucmdb-rest.svg)](https://pypi.org/project/ucmdb-rest/)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/pypi/dm/ucmdb-rest.svg)](https://pypi.org/project/ucmdb-rest/)

A modern, object-oriented Python 3.6+ client for the OpenText Universal Configuration Management Database (UCMDB) REST API. This library eliminates boilerplate by centralizing authentication, session persistence, and pagination through a single unified `UCMDBServer` entry point — so you can focus on what you want to do, not how to connect.

```bash
pip install ucmdb-rest
```

## Why This Library?

Working directly with the UCMDB REST API means managing token authentication, handling session expiry, manually paginating large result sets, and remembering the correct endpoint paths for each operation. `ucmdb-rest` handles all of that for you through a clean, modular, object-oriented interface with type-safe Enums throughout.

## Quick Start

```python
from ucmdb_rest import UCMDBServer

# Initialize client from credentials file
client = UCMDBServer.from_json('credentials.json')

# Quick connectivity check
print(f"Connected to: {client.server_version}")

# Get detailed version info
version = client.system.getUCMDBVersion().json()
print(f"Product: {version['productName']}")
print(f"Content Pack: {version['contentPackVersion']}")
```

## Setup and Authentication

Examples in this library assume a `credentials.json` file in the same directory as your script.

1. Copy `credentials.json.example` to `credentials.json`
2. Update the values with your UCMDB server details

| Key | Description |
| :--- | :--- |
| **user** | UCMDB Username |
| **password** | UCMDB Password |
| **server** | FQDN or IP of the UCMDB Server |
| **port** | REST API port (Default 8443) |
| **ssl_validation** | Boolean (`false` to skip certificate checks in lab environments) |

## Functional Modules

The library mirrors the UCMDB API ecosystem with domain-specific modules:

| Module | Description |
| :--- | :--- |
| **client** | `UCMDBServer` class — the unified entry point for all operations. |
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

## Practical Examples

Ready-to-run scripts are included in the [Examples](https://github.com/kwpaschal/ucmdb_rest/tree/main/Examples) directory:

| Script | Description |
| :--- | :--- |
| `add_cis.py` | Create CIs and Relationships with custom properties |
| `delete_cis.py` | Delete CIs by their UCMDB ID |
| `get_recon_rule.py` | Display a reconciliation rule for a CI Type |
| `initialize_get_version.py` | Display version information about the UCMDB Server |
| `query_topology.py` | Run a UCMDB View and retrieve the results |
| `search_and_expose_ci.py` | Search for a CI by name and get specific properties |
| `show_content_packs.py` | Display current content pack information |
| `show_license_report.py` | Display a license report from UCMDB |

## Documentation

Full API reference is available at **[kwpaschal.github.io/ucmdb_rest](https://kwpaschal.github.io/ucmdb_rest/)**, powered by MkDocs with Material theme and mkdocstrings (numpy-style docstrings).

```bash
# Preview documentation locally
mkdocs serve
```

## Development and Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run full test suite with coverage
pytest --cov=ucmdb_rest
```

## Release History

* **2.0.3 (Current)**
  * Improved README with badges, Why This Library section, and documentation links
* **2.0.2**
  * Packaging and metadata updates
* **2.0.1**
  * Fixed failing tests
  * Added example scripts
* **2.0.0** — Major Architecture Milestone
  * Completed migration of all legacy `rest.py` components
  * Re-engineered core modules into a modular, object-oriented framework
  * Standardized response handling using `requests.Response` objects across all modules
  * Enhanced code discoverability via the unified `UCMDBServer` entry point
* **1.6.0** — Added Settings and Recipients management
* **1.5.0** — Added Reports functionality and tests
* **1.4.0** — Added Management Zone functionality and tests
* **1.3.0** — Added LDAP configuration retrieval
* **1.2.0** — Added integration point retrieval
* **1.1.0** — Added ExposeCI ad-hoc query support
* **1.0.0** — Initial stable release: Topology and Discovery modules complete

## License

MIT License — see [LICENSE](LICENSE) for details.
