# ucmdb_rest Test Suite

Comprehensive test suite for the ucmdb_rest library with full coverage of version checking infrastructure and API functions.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── test_version_checking.py    # Unit tests for version infrastructure
├── test_integration.py         # Integration tests (mocked and live)
├── run_tests.py               # Test runner script
└── README.md                  # This file
```

## Running Tests

### Quick Start

```bash
# Run all tests (mocked mode)
python tests/run_tests.py

# Run with verbose output
python tests/run_tests.py -v

# Run with coverage report
python tests/run_tests.py --coverage
```

### Using unittest

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_version_checking -v

# Run specific test class
python -m unittest tests.test_version_checking.TestVersionComparison -v

# Run specific test method
python -m unittest tests.test_version_checking.TestVersionComparison.test_mixed_format_comparison -v
```

### Live Testing

To run tests against real UCMDB servers:

```bash
# Requires credentials.json in ucmdb_rest/discovery/
python tests/run_tests.py --live
```

**Note**: Live tests are skipped by default. Set `UCMDB_TEST_LIVE=true` environment variable or use `--live` flag.

## Test Coverage

### Unit Tests (`test_version_checking.py`)

Tests the core version checking infrastructure without external dependencies:

- **TestVersionNormalization**: Version string parsing
  - YYYY.MM format (e.g., 2023.05)
  - YY.Q format (e.g., 23.4 = Q4 2023)

- **TestVersionComparison**: Version comparison logic
  - Same format comparisons
  - Mixed format comparisons
  - Edge cases

- **TestRequiresVersionDecorator**: Decorator functionality
  - Allows compatible versions
  - Blocks incompatible versions
  - Caches version info
  - Gracefully handles errors

- **TestVersionCacheClearing**: Cache management
  - Cache clearing functionality

### Integration Tests (`test_integration.py`)

Tests actual function calls with mocked or real UCMDB servers:

- **TestAuthenticationWithVersionChecking**: Auth + version retrieval
- **TestFunctionsWithMockedVersions**: API calls with version checks
- **TestEndToEndWorkflow**: Complete workflows

## Writing New Tests

### Unit Test Example

```python
import unittest
from ucmdb_rest.utils import compare_versions

class TestMyFeature(unittest.TestCase):
    def test_something(self):
        """Test description"""
        result = compare_versions("24.2", "23.4")
        self.assertTrue(result)
```

### Integration Test Example

```python
import unittest
from unittest.mock import Mock, patch

class TestMyIntegration(unittest.TestCase):
    @unittest.skipUnless(LIVE_MODE, "Skipping live test")
    def test_live_feature(self):
        """Test against real server"""
        # Test code here
        pass
```

## Continuous Integration

The test suite runs automatically on:
- Every push to `main` or `develop` branches
- Every pull request

See `.github/workflows/tests.yml` for CI configuration.

## Test Results

### Current Status

- ✅ All unit tests passing (10/10)
- ✅ All integration tests passing (mocked mode)
- ⏸ Live tests require credentials

### Coverage Goals

- Unit tests: 100% coverage of version checking code
- Integration tests: 100% coverage of all 26 tested API functions
- End-to-end tests: Complete workflows from auth to data retrieval

## Troubleshooting

### Tests Fail with "Module not found"

Ensure you're running from the project root:
```bash
cd /path/to/ucmdb_rest
python tests/run_tests.py
```

### Live Tests Skip

Live tests require:
1. `ucmdb_rest/discovery/credentials.json` file
2. `UCMDB_TEST_LIVE=true` environment variable or `--live` flag

### Coverage Not Working

Install coverage module:
```bash
pip install coverage
```

## Contributing

When adding new features:

1. Write unit tests first (TDD approach)
2. Add integration tests for API functions
3. Update this README if adding new test categories
4. Ensure all tests pass before committing

## Future Enhancements

- [ ] Add tests for remaining 62 untested API functions
- [ ] Add performance/load testing
- [ ] Add security testing (credential handling, SSL validation)
- [ ] Add mutation testing for better coverage validation
- [ ] Create test fixtures for common scenarios
