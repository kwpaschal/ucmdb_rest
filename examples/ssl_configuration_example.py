#!/usr/bin/env python3
"""
Example: How to configure SSL certificate verification

This example demonstrates different ways to configure SSL certificate
verification in the ucmdb_rest library.
"""

import ucmdb_rest

# Example 1: Development Environment (default)
# ---------------------------------------------
print("=" * 60)
print("Example 1: Development Environment (No SSL Verification)")
print("=" * 60)

# Explicitly set to False (this is the default)
ucmdb_rest.set_verify_ssl(False)

# Create connection
token = ucmdb_rest.createHeaders(
    'admin',
    'admin',
    '192.168.1.100',
    port=8443
)

# All API calls will use verify=False
print(f"Current SSL setting: {ucmdb_rest.get_verify_ssl()}")
print("✓ SSL verification disabled - for testing only!\n")


# Example 2: Production Environment (SSL Enabled)
# -----------------------------------------------
print("=" * 60)
print("Example 2: Production Environment (SSL Verification Enabled)")
print("=" * 60)

# Enable SSL verification for production
ucmdb_rest.set_verify_ssl(True)

# Create connection to production server with valid cert
token_prod = ucmdb_rest.createHeaders(
    'api_user',
    'secure_password',
    'ucmdb.mycompany.com',
    port=8443
)

print(f"Current SSL setting: {ucmdb_rest.get_verify_ssl()}")
print("✓ SSL verification enabled - secure for production!\n")


# Example 3: Custom CA Bundle
# ----------------------------
print("=" * 60)
print("Example 3: Custom CA Bundle (Self-Signed Certificate)")
print("=" * 60)

# Use custom CA bundle for self-signed or internal CA
ucmdb_rest.set_verify_ssl('/etc/ssl/certs/mycompany-ca-bundle.crt')

# Create connection
token_custom = ucmdb_rest.createHeaders(
    'admin',
    'password',
    'ucmdb-internal.mycompany.local',
    port=8443
)

print(f"Current SSL setting: {ucmdb_rest.get_verify_ssl()}")
print("✓ Using custom CA bundle for internal certificates!\n")


# Example 4: Environment-Based Configuration
# ------------------------------------------
print("=" * 60)
print("Example 4: Environment-Based Configuration")
print("=" * 60)

import os

# Read from environment variable
env_verify = os.getenv('UCMDB_VERIFY_SSL', 'False')

if env_verify.lower() == 'true':
    ucmdb_rest.set_verify_ssl(True)
    print("SSL verification ENABLED (from environment)")
elif os.path.exists(env_verify):
    ucmdb_rest.set_verify_ssl(env_verify)
    print(f"Using CA bundle: {env_verify}")
else:
    ucmdb_rest.set_verify_ssl(False)
    print("SSL verification DISABLED (from environment)")

print(f"Current SSL setting: {ucmdb_rest.get_verify_ssl()}\n")


# Example 5: Configuration from JSON File
# ----------------------------------------
print("=" * 60)
print("Example 5: Load Configuration from JSON File")
print("=" * 60)

import json

# Example config file content
config_example = {
    "ucmdb_server": "ucmdb.example.com",
    "port": 8443,
    "verify_ssl": True,  # or False, or "/path/to/ca.crt"
    "username": "admin"
}

# In real code, you would load from file:
# with open('config.json') as f:
#     config = json.load(f)

# Set SSL verification from config
ucmdb_rest.set_verify_ssl(config_example['verify_ssl'])

print(f"Loaded config: {config_example}")
print(f"Current SSL setting: {ucmdb_rest.get_verify_ssl()}")
print("✓ Configuration loaded from file!\n")


# Summary
print("=" * 60)
print("Summary")
print("=" * 60)
print("""
SSL verification can be configured in three ways:

1. False (default)     - Disable SSL verification (testing only)
2. True                - Enable SSL verification (production)
3. "/path/to/ca.crt"   - Use custom CA bundle (self-signed certs)

Choose the appropriate setting based on your environment:
- Development/Testing: verify_ssl = False
- Production:          verify_ssl = True
- Internal CA:         verify_ssl = "/path/to/internal-ca.crt"

For more information, see SSL_CONFIGURATION.md
""")
