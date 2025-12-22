# TODO List for ucmdb_rest

## High Priority - PyPI Publication Readiness

### Required Before PyPI Upload
- [ ] Create LICENSE file (choose: MIT, Apache 2.0, BSD, etc.)
- [ ] Rename `readme.md` to `README.md` (case sensitivity for PyPI)
- [ ] Update setup.py:
  - [ ] Fix GitHub URL (line 17) - currently points to placeholder
  - [ ] Update version to 1.2.0 or 2.0.0 (added version checking features)
  - [ ] Ensure license in classifiers matches LICENSE file
- [ ] Expand README.md with:
  - [ ] Installation instructions (`pip install ucmdb_rest`)
  - [ ] Quick start example code
  - [ ] Version compatibility table (which UCMDB versions are supported)
  - [ ] Link to documentation
  - [ ] Requirements and dependencies
  - [ ] Contribution guidelines
- [ ] Create CHANGELOG.md documenting all releases and changes

### Documentation
- [ ] Create `examples/` directory with sample scripts:
  - [ ] Basic authentication example
  - [ ] Query CIs example
  - [ ] Package deployment example
  - [ ] Discovery job management example
- [ ] Add docstring examples to key functions
- [ ] Create API reference documentation (consider Sphinx)

### Testing Improvements
- [ ] Add end-to-end integration tests for state-dependent operations:
  - [ ] Create test CI → Update test CI → Delete test CI
  - [ ] Create test package → Delete test package
  - [ ] Create test job group → Delete test job group
  - [ ] Create test recipient → Update recipient → Delete recipient
  - [ ] Create test management zone → Delete management zone
- [ ] Add setup/teardown methods for integration tests
- [ ] Use unique test identifiers to avoid conflicts (e.g., timestamp-based names)
- [ ] Add test fixtures for common scenarios
- [ ] Consider adding property-based testing (hypothesis library)
- [ ] Add performance/load testing for bulk operations

### Version Checking - Apply Decorators to Remaining Functions
Currently applied to: utils.py (documented), packages.py (2 functions)

Still need decorators on:
- [ ] datamodel.py (2 functions: getClass, retrieveIdentificationRule)
- [ ] topology.py (1 function: queryCIs)
- [ ] policies.py (2 functions: getPolicies, getComplainceViews)
- [ ] discovery.py (6 functions: getJobGroup, getJobMetaData, getSchedules, getModuleTree, getIPRange, getUseCase)
- [ ] dataflowmanagment.py (6 functions: getAllCredentials, getCredentialProfiles, getAllDomains, getAllProtocols, getProbeInfo, probeStatus)
- [ ] mgmtzone.py (1 function: getMgmtZone)
- [ ] settings.py (1 function: getRecipients)
- [ ] integration.py (1 function: getIntegrationInfo)
- [ ] ldap.py (1 function: getLDAPSettings)

Note: Need to determine minimum UCMDB version for each function through testing

### Code Quality
- [ ] Add type hints throughout the codebase (Python 3.6+ compatible)
- [ ] Set up pre-commit hooks:
  - [ ] Black formatter
  - [ ] Flake8 linter
  - [ ] isort for import sorting
  - [ ] mypy for type checking
- [ ] Add docstring validation (pydocstyle)
- [ ] Increase test coverage to 90%+ (currently focused on version checking only)

### Security
- [ ] Add security testing for credential handling
- [ ] Review SSL certificate validation (currently verify=False in many places)
- [ ] Add warnings for insecure usage patterns
- [ ] Consider adding support for secure credential storage (keyring, env vars)
- [ ] Add input validation to prevent injection attacks

### Features
- [ ] Add async/await support for concurrent API calls
- [ ] Add retry logic with exponential backoff for failed requests
- [ ] Add request/response logging (optional debug mode)
- [ ] Add progress bars for long-running operations (tqdm)
- [ ] Create CLI tool for common operations
- [ ] Add caching for expensive read operations
- [ ] Support for UCMDB API pagination on large result sets

### CI/CD
- [ ] Set up GitHub Actions to publish to PyPI on release tag
- [ ] Add automated version bumping
- [ ] Add code coverage reporting (codecov.io)
- [ ] Add automated dependency updates (Dependabot)
- [ ] Set up pre-release/beta channel on PyPI

### Community
- [ ] Add CONTRIBUTING.md with development setup instructions
- [ ] Add CODE_OF_CONDUCT.md
- [ ] Create issue templates for bug reports and feature requests
- [ ] Add pull request template
- [ ] Set up GitHub Discussions for Q&A
- [ ] Add badges to README (build status, coverage, PyPI version, downloads)

## Low Priority / Nice to Have

### Documentation
- [ ] Create readthedocs.io site
- [ ] Add architecture diagrams
- [ ] Create video tutorials
- [ ] Add FAQ section

### Testing
- [ ] Add mutation testing (mutpy)
- [ ] Add contract testing for API compatibility
- [ ] Add stress testing for rate limiting

### Features
- [ ] Add GraphQL support (if UCMDB adds it)
- [ ] Create Jupyter notebook examples
- [ ] Add support for UCMDB webhooks/callbacks
- [ ] Create plugin system for custom extensions

## Notes

### Testing Strategy
- Unit tests (mocked) - Fast, run on every commit
- Integration tests (mocked) - Medium speed, run on every commit
- End-to-end tests (live servers) - Slow, run before releases only
- Live server tests should only run in "crash and burn" test environments
- Use Keith's existing long test script as reference for E2E test patterns

### Version Compatibility
- Test against UCMDB versions: 2023.05, 23.4, 24.2, 24.4, 25.2, 25.3, 25.4
- When new UCMDB version releases, add to test matrix
- Document which Python versions are supported (currently 3.6+)

### Release Process
1. Run full test suite (including live tests on test servers)
2. Update version in setup.py
3. Update CHANGELOG.md
4. Create git tag
5. Push to GitHub
6. GitHub Actions publishes to PyPI automatically
