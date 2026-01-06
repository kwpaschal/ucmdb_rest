# SSL Certificate Verification Configuration

## Overview

The `ucmdb_rest` library allows you to configure SSL certificate verification for all UCMDB REST API calls. By default, SSL verification is **disabled** (`verify=False`) for backwards compatibility with test environments that may not have valid SSL certificates.

## Security Warning

⚠️ **IMPORTANT**: Disabling SSL verification (the default) is **insecure** and should only be used in test/development environments. Production systems should always use valid SSL certificates and enable verification.

## Configuration Methods

### Method 1: Global Configuration (Recommended)

Set the SSL verification globally at the start of your script:

```python
import ucmdb_rest

# Disable SSL verification (default - for test environments only)
ucmdb_rest.set_verify_ssl(False)

# Enable SSL verification (recommended for production)
ucmdb_rest.set_verify_ssl(True)

# Use custom CA bundle file
ucmdb_rest.set_verify_ssl('/path/to/custom-ca-bundle.crt')
```

### Method 2: Check Current Setting

You can check the current SSL verification setting:

```python
import ucmdb_rest

current_setting = ucmdb_rest.get_verify_ssl()
print(f"SSL verification is set to: {current_setting}")
```

## Usage Examples

### Example 1: Development Environment (No Valid Certificates)

```python
import ucmdb_rest

# Explicitly disable SSL verification for test environment
ucmdb_rest.set_verify_ssl(False)

# Create authentication headers
token = ucmdb_rest.createHeaders(
    'admin',
    'password',
    '192.168.1.100',
    port=8443
)

# All subsequent API calls will use verify=False
version_data = ucmdb_rest.getUCMDBVersion(token, '192.168.1.100')
print(f"UCMDB Version: {version_data.json()}")
```

### Example 2: Production Environment (Valid Certificates)

```python
import ucmdb_rest

# Enable SSL verification for production
ucmdb_rest.set_verify_ssl(True)

# Create authentication headers
token = ucmdb_rest.createHeaders(
    'api_user',
    'secure_password',
    'ucmdb.mycompany.com',
    port=8443
)

# All API calls will verify SSL certificates
cis = ucmdb_rest.queryCIs(token, 'ucmdb.mycompany.com', query_definition)
```

### Example 3: Custom CA Bundle

If your UCMDB server uses a self-signed certificate or internal CA:

```python
import ucmdb_rest

# Use custom CA bundle
ucmdb_rest.set_verify_ssl('/etc/ssl/certs/mycompany-ca-bundle.crt')

# Create authentication headers
token = ucmdb_rest.createHeaders(
    'admin',
    'password',
    'ucmdb-internal.mycompany.local',
    port=8443
)

# API calls will verify using your custom CA bundle
packages = ucmdb_rest.getPackages(token, 'ucmdb-internal.mycompany.local')
```

## Configuration Values

The `set_verify_ssl()` function accepts three types of values:

| Value | Type | Description | Use Case |
|-------|------|-------------|----------|
| `False` | bool | Disable SSL verification (default) | Test/dev environments without valid certs |
| `True` | bool | Enable SSL verification using system CA bundle | Production with valid public certificates |
| `/path/to/ca.crt` | str | Path to custom CA bundle file | Self-signed or internal CA certificates |

## Best Practices

### Development/Testing
```python
# At the top of your test scripts
import ucmdb_rest
ucmdb_rest.set_verify_ssl(False)

# Consider adding a warning
import warnings
warnings.warn("SSL verification is DISABLED - for testing only!")
```

### Production
```python
# At the top of your production scripts
import ucmdb_rest
ucmdb_rest.set_verify_ssl(True)

# Or use environment variable
import os
verify_ssl = os.getenv('UCMDB_VERIFY_SSL', 'True').lower() == 'true'
ucmdb_rest.set_verify_ssl(verify_ssl)
```

### Configuration File
```python
import ucmdb_rest
import json

# Load configuration from file
with open('config.json') as f:
    config = json.load(f)

ucmdb_rest.set_verify_ssl(config.get('verify_ssl', False))
```

## Troubleshooting

### SSL Certificate Verification Failed

If you see errors like:
```
SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

**Solutions:**

1. **For production**: Ensure your UCMDB server has a valid SSL certificate from a trusted CA
2. **For internal CA**: Use the path to your CA bundle:
   ```python
   ucmdb_rest.set_verify_ssl('/path/to/internal-ca-bundle.crt')
   ```
3. **For development only**: Disable verification (not recommended):
   ```python
   ucmdb_rest.set_verify_ssl(False)
   ```

### Warnings About Unverified HTTPS Requests

If you see:
```
InsecureRequestWarning: Unverified HTTPS request is being made to host 'ucmdb.example.com'
```

This means SSL verification is disabled. To suppress the warning:

```python
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress the warning (if intentionally using verify=False)
warnings.filterwarnings('ignore', category=InsecureRequestWarning)
```

**Better solution**: Enable SSL verification with valid certificates instead of suppressing the warning.

## Migration Guide

If you're upgrading from an older version of `ucmdb_rest` that used `verify_flag` parameters:

### Before (Old Code)
```python
# Old code with verify_flag parameter
response = ucmdb_rest.addCIs(
    token,
    server,
    ci_data,
    verify_flag=False  # No longer supported
)
```

### After (New Code)
```python
# Set globally at script start
import ucmdb_rest
ucmdb_rest.set_verify_ssl(False)

# Then call without verify_flag
response = ucmdb_rest.addCIs(
    token,
    server,
    ci_data
)
```

## Default Behavior

If you don't call `set_verify_ssl()`, the default behavior is:
- **SSL verification is DISABLED** (`verify=False`)
- This maintains backwards compatibility with existing scripts
- You will see SSL warnings in the output (unless suppressed)

## Related Links

- [Python Requests SSL Verification](https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification)
- [urllib3 SSL/TLS Documentation](https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings)
- [Creating Custom CA Bundles](https://requests.readthedocs.io/en/latest/user/advanced/#ca-certificates)
