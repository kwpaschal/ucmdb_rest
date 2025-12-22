"""
Configuration module for ucmdb_rest library

This module provides global configuration options that affect all API calls.
"""

# Global SSL certificate verification setting
# Set to False to disable SSL certificate verification (default for backwards compatibility)
# Set to True to enable SSL certificate verification
# Can also be set to a path to a CA bundle file
VERIFY_SSL = False


def set_verify_ssl(verify):
    """
    Configure SSL certificate verification for all UCMDB API calls.

    Args:
        verify: Can be one of:
                - False: Disable SSL verification (default, not recommended for production)
                - True: Enable SSL verification using system CA bundle
                - str: Path to CA bundle file for verification

    Example:
        import ucmdb_rest

        # Disable SSL verification (default)
        ucmdb_rest.set_verify_ssl(False)

        # Enable SSL verification
        ucmdb_rest.set_verify_ssl(True)

        # Use custom CA bundle
        ucmdb_rest.set_verify_ssl('/path/to/ca-bundle.crt')

    Note:
        Disabling SSL verification (verify=False) is insecure and should only be used
        in test/development environments. Production systems should always use valid
        SSL certificates and enable verification.
    """
    global VERIFY_SSL
    VERIFY_SSL = verify


def get_verify_ssl():
    """
    Get the current SSL verification setting.

    Returns:
        The current verify setting (False, True, or path to CA bundle)
    """
    return VERIFY_SSL
