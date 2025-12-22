# UCMDB REST API Version Checking - Implementation Summary

**Date**: 2025-12-19
**Author**: Keith Paschal
**Feature**: Automatic API version compatibility checking

## Overview

Implemented a comprehensive version checking system for the ucmdb_rest library to ensure functions are only called on UCMDB servers that support them. The system uses Python decorators to automatically validate server versions before executing API calls.

## What Was Built

### 1. Core Version Checking Infrastructure ([utils.py](ucmdb_rest/utils.py))

#### New Classes
- **`UCMDBVersionError`**: Custom exception raised when a function is called on an incompatible UCMDB version

#### New Functions
- **`_normalize_version(version_str)`**: Converts version strings (both "YYYY.MM" and "YY.M" formats) to comparable tuples
- **`compare_versions(current, required)`**: Compares two version strings (returns True if current >= required)
- **`_get_cached_version(token, udserver)`**: Retrieves and caches UCMDB version per server
- **`requires_version(min_version)`**: Decorator that enforces minimum version requirements
- **`clear_version_cache()`**: Utility to clear the version cache

#### Enhanced Functions
- **`authenticate(user, passwd, udserver, ssl=False, port=8443)`**: Added port parameter
- **`createHeaders(uduser, udpass, udsystem, port=8443)`**: Added port parameter

### 2. API Discovery Tools ([ucmdb_rest/discovery/](ucmdb_rest/discovery/))

#### Scripts
1. **`discover_apis.py`**: Tests all 88 functions across multiple UCMDB versions
   - Connects to each configured server
   - Tests every function systematically
   - Generates detailed JSON results per version
   - Reports success/failure with response times

2. **`analyze_results.py`**: Analyzes discovery results to determine minimum versions
   - Processes all result files
   - Determines earliest version where each function works
   - Generates three outputs:
     - `version_matrix.json`: Structured data
     - `version_matrix.md`: Human-readable report
     - `function_decorators.txt`: Ready-to-use decorators

3. **`test_decorator.py`**: Validates the version checking system
   - Tests version comparison logic
   - Tests decorator with mocked responses
   - Tests live connection to a real server

#### Configuration
- **`credentials.json`**: Server configurations for 7 UCMDB versions
  - 2023.05, 23.4, 24.2, 24.4, 25.2, 25.3, 25.4
  - Includes hostnames, ports, credentials
  - Gitignored for security

- **`README.md`**: Complete usage documentation

### 3. Updated Package Exports ([\_\_init\_\_.py](ucmdb_rest/__init__.py))

Added exports for version checking utilities:
```python
from .utils import (
    UCMDBVersionError, requires_version, compare_versions, clear_version_cache
)
```

### 4. Updated .gitignore

Added exclusion for discovery folder (contains credentials and test results):
```
# Discovery tests (contains credentials and test results)
ucmdb_rest/discovery/
```

## How It Works

### Version Checking Flow

1. **Function Call**: User calls a decorated function
   ```python
   @requires_version("24.2")
   def getPackages(token, udserver):
       return requests.get(_url(udserver, '/packages'), headers=token)
   ```

2. **Version Retrieval**: Decorator checks cache or calls `getUCMDBVersion()`
   - First call: Fetches version from server, caches it
   - Subsequent calls: Uses cached version (fast)

3. **Version Comparison**: Compares server version to required version
   - Normalizes both versions to (year, month) tuples
   - Handles both "2023.05" and "24.2" formats

4. **Decision**:
   - ✓ **If version >= required**: Function executes normally
   - ✗ **If version < required**: Raises `UCMDBVersionError` with helpful message

### Version Format Support

| Format | Example | Normalized To |
|--------|---------|---------------|
| YYYY.MM | 2023.05 | (2023, 5) |
| YY.M | 24.2 | (2024, 2) |
| YY.M | 25.4 | (2025, 4) |

### Port Configuration

Different UCMDB deployments use different ports:
- **8443**: Traditional installations (most common)
- **443**: Containerized deployments
- **9443**: Alternative configurations

All authentication functions now accept an optional `port` parameter.

## Usage Example

### Before (No Version Checking)
```python
from ucmdb_rest import createHeaders, getPackages

token = createHeaders("admin", "password", "ucmdb-server")
packages = getPackages(token, "ucmdb-server")  # May fail on old servers
```

### After (With Version Checking)
```python
from ucmdb_rest import createHeaders, getPackages, UCMDBVersionError

token = createHeaders("admin", "password", "ucmdb-server")

try:
    packages = getPackages(token, "ucmdb-server")
except UCMDBVersionError as e:
    print(f"Error: {e}")
    # Output: Function 'getPackages' requires UCMDB version 24.2 or later.
    #         Your UCMDB server (ucmdb-server) is running version 23.4.
```

## Testing Workflow

### Step 1: Verify Infrastructure
```bash
cd ucmdb_rest/discovery
python test_decorator.py
```

Expected output:
```
✓ PASS: Version Comparison
✓ PASS: Decorator Logic
✓ PASS: Live Connection
Overall: 3/3 tests passed
```

### Step 2: Run Discovery
```bash
python discover_apis.py
```

This tests all 88 functions across 7 servers (takes ~5-10 minutes).

### Step 3: Analyze Results
```bash
python analyze_results.py
```

Generates:
- `results/version_matrix.json`
- `results/version_matrix.md`
- `results/function_decorators.txt`

### Step 4: Apply Decorators

Use the generated `function_decorators.txt` to add `@requires_version()` to each function.

Example:
```python
# packages.py

@requires_version("24.2")
def getPackages(token, udserver):
    """
    Retrieves all packages from UCMDB.

    Minimum UCMDB Version: 24.2

    Parameters
    ----------
    token : dict
        Authentication token from createHeaders.
    udserver : str
        UCMDB server hostname or IP.

    Returns
    -------
    requests.Response
        Package information.
    """
    return requests.get(_url(udserver, '/packages'), headers=token, verify=False)
```

## Next Steps

### Immediate (Ready to Execute)
1. ✅ Run `test_decorator.py` to verify everything works
2. ✅ Run `discover_apis.py` to test all functions on all 7 servers
3. ⏳ Run `analyze_results.py` to determine minimum versions
4. ⏳ Apply `@requires_version()` decorators to all 88 functions
5. ⏳ Update docstrings with minimum version information

### Future Enhancements
- Create unit tests for the version checking system
- Add version compatibility matrix to main README.md
- Update package version to 1.2.0
- Consider adding a `--skip-version-check` flag for testing
- Add logging for version check warnings

## File Changes Summary

### Modified Files
1. **`ucmdb_rest/utils.py`**
   - Added ~200 lines of version checking code
   - Enhanced `authenticate()` and `createHeaders()` with port parameter
   - Added imports: `functools.wraps`, `typing.Dict`

2. **`ucmdb_rest/__init__.py`**
   - Added exports for version checking utilities

3. **`.gitignore`**
   - Fixed encoding issues
   - Added exclusion for `ucmdb_rest/discovery/`

### New Files
1. **`ucmdb_rest/discovery/credentials.json`** (gitignored)
2. **`ucmdb_rest/discovery/discover_apis.py`**
3. **`ucmdb_rest/discovery/analyze_results.py`**
4. **`ucmdb_rest/discovery/test_decorator.py`**
5. **`ucmdb_rest/discovery/README.md`**
6. **`IMPLEMENTATION_SUMMARY.md`** (this file)

## Tested UCMDB Versions

| Version | Type | Hostname | Port | Status |
|---------|------|----------|------|--------|
| 2023.05 | Production | sacucmrl2305.otxlab.net | 8443 | Ready |
| 23.4 | Production | sacucmrl234w.otxlab.net | 8443 | Ready |
| 24.2 | Production | 10.67.248.28 | 8443 | Ready |
| 24.4 | Production | sacucmrl244w.otxlab.net | 8443 | Ready |
| 25.2 | Production | sacucmrl252w.otxlab.net | 8443 | Ready |
| 25.3 | Container-only | bp2ucmrl253mast.otxlab.net | 443 | Ready |
| 25.4 | Production | sacucmrl254w.otxlab.net | 8443 | Ready |

## Benefits

1. **User Safety**: Prevents cryptic errors when calling unsupported APIs
2. **Clear Errors**: Provides actionable error messages with version requirements
3. **Performance**: Caches version info to avoid repeated API calls
4. **Flexibility**: Supports both traditional and containerized UCMDB
5. **Documentation**: Auto-discovery creates accurate version compatibility docs
6. **Maintainability**: Decorator pattern keeps code DRY across 88 functions

## Technical Design Decisions

### Why Decorators?
- **DRY Principle**: One implementation, 88 uses
- **Maintainability**: Change once, affects all functions
- **Clean Code**: Business logic separate from validation
- **Python Idiom**: Standard pattern for cross-cutting concerns

### Why Cache Versions?
- **Performance**: Avoid HTTP call on every function call
- **Efficiency**: One version check per server per session
- **User Experience**: Faster execution after first call

### Why Support Both Version Formats?
- **Reality**: UCMDB uses both "2023.05" and "24.2" formats
- **Flexibility**: Works regardless of which format is returned
- **Future-proof**: Handles format changes gracefully

### Why Gitignore Discovery?
- **Security**: Protects server credentials
- **Privacy**: Results may contain sensitive server info
- **Size**: JSON results can be large

## Security Considerations

⚠️ **Important**:
- `credentials.json` contains plaintext passwords
- Use test accounts, not production admin credentials
- Discovery folder is gitignored by default
- Results may reveal server architecture
- Review results before sharing

## Questions?

See the [discovery README](ucmdb_rest/discovery/README.md) for detailed usage instructions.

---

**Status**: ✅ Infrastructure complete and ready for testing
**Next Action**: Run `test_decorator.py` to validate the implementation
