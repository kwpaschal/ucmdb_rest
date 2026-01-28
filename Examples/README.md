# UCMDB Python REST Library Examples

This directory contains practical scripts demonstrating how to use the `ucmdb_rest` library to automate common UCMDB tasks.

## Setup & Authentication

All examples in this directory use a shared `credentials.json` file for authentication. 

1. Copy `credentials.json.example` to `credentials.json`.
2. Update the values with your server details and credentials:

```json
{
  "user": "admin",
  "password": "your_password",
  "server": "ucmdb-server.example.com",
  "port": 8443,
  "ssl_validation": false
}
```
# Available Examples
## Data Management
* `add_cis.py`: Demonstrates how to push new CIs and Relationships into UCMDB.
* `delete_cis.py`: Shows how to remove specific CIs from UCMDB using their UCMDB IDs.
* `search_and_expose_ci.py`: Uses the powerful `search_by_label` function to find CIs 
matching a pattern (e.g. %Server%) and retrieve specific attributes in one request
## Discovery and Troubleshooting
* `get_recon_rule.py`: Displays the identification rule (reconciliation rule) for a specific
CI Type and decodes the Base64 `ruleXml` for easy reading
* `query_topology.py`: Executes a named TQL or View and retrieves the resulting topology map
## System Reporting
* `initialize_get_version.py`: A simple 'Hello World' script to test the connection and display
UCMDB Server information
* `show_content_packs.py`: Displays the version and deployment status of Content Packs
* `show_license_report.py`: Displays an audit of the licence consumption breaking down by unit type
## Usage
To run any example, ensure you are in the root directory of the project and run:
```
bash
python Examples/search_and_expose_ci.py
```