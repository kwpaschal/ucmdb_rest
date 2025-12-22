"""
Created on Wed Jun  5 14:35:37 2024

@author: kpaschal

This library contains methods to access the UCMDB REST-API.

Version 1.0
-----------
Converted to Python 3.13
Split Utilities into separate file

"""

import requests
import sys
import json
from functools import wraps
from typing import Dict
from . import config

def addCIQuestions():
    """
    This method asks a bunch of questions to pass back specific values
    to be used in the addCIs method.

    Returns
    -------
    tuple
        A tuple containing the following boolean values:
        globalIDs, forceTemp, ignoreExisting, returnIDs,
        ignoreCantId, shouldVerify. For example:
        (True, False, True, False, True, True)

    """
    globalIDs = strToBool(
        input('Does the CI Definition include a valid global ID? (Yes or No): ')
    )
    forceTemp = strToBool(
        input('Does the CI definition contain temporary IDs? (Yes or No): ')
    )
    ignoreExisting = strToBool(
        input('Should existing CIs be ignored? (Yes or No): ')
    )
    returnIDs = strToBool(
        input('Should an ID map be returned mapping the ID in the CI definition '
              'to their global IDs generated in UCMDB? (Yes or No): ')
    )
    ignoreCantId = strToBool(
        input('If a CI cannot be identified, should it be ignored? (Yes or No): ')
    )
    shouldVerify = strToBool(
        input('Should the SSL certificate in UCMDB be verified? (Yes or No): ')
    )
    return (globalIDs, forceTemp, ignoreExisting, returnIDs, ignoreCantId,
            shouldVerify)


def authenticate(user, passwd, udserver, ssl=False, port=8443):
    """
    Authenticates a user with a POST call to the UCMDB server.

    This function uses the `_url` method to construct the URL for
    connecting to the UCMDB server. SSL is parameterized as False
    by default but can be set to True if SSL certificate validation
    is required.

    Parameters
    ----------
    user : str
        UCMDB username.
    passwd : str
        UCMDB password.
    udserver : str
        UCMDB server IP or hostname.
    ssl : bool, optional
        Whether to validate the SSL certificate. Defaults to False.
    port : int, optional
        The port number for UCMDB server. Defaults to 8443.
        Common ports: 443 (containerized), 8443 (traditional), 9443.

    Returns
    -------
    requests.Response
        The response from the authenticate REST-API method in UCMDB.

    Raises
    ------
    requests.exceptions.ConnectionError
        If the UCMDB server is not installed or not running, this error
        is caught and a message is printed.

    Example
    -------
    >>> response = authenticate('admin', 'password', '127.0.0.1', ssl=True)
    >>> response.status_code
    200
    >>> response = authenticate('admin', 'password', 'container.example.com', port=443)
    >>> response.status_code
    200
    """
    payload = {
        'username': user,
        'password': passwd,
        'clientContext': '1'
    }
    try:
        return requests.post(_url(udserver, '/authenticate', port=port), json=payload,
                             verify=ssl)
    except requests.exceptions.ConnectionError:
        print('Server is either not installed or not running')
        sys.exit()

def _url(udserver, path, port=8443):
    """
    Builds the URL to access UCMDB via the REST API.

    Parameters
    ----------
    udserver : str
        UCMDB server IP or hostname.
    path : str
        The path after the rest-api part of the string.
    port : int, optional
        The default is 8443.

    Returns
    -------
    str
        Returns a string which is the completed URL to use for the REST
        API call which is needed. For example:
            https://myucmdb.mycompany.com:8443/rest-api/authenticate

    """
    # print("Path is: https://", udserver, ":8443/rest-api", path, sep='')
    return 'https://' + udserver + ':' + str(port) + '/rest-api' + path


def createHeaders(uduser, udpass, udsystem, port=8443):
    """
    Creates a header for the UCMDB server.

    Parameters
    ----------
    uduser : str
        UCMDB Username.
    udpass : str
        UCMDB Password.
    udsystem : str
        UCMDB Server hostname/IPV4.
    port : int, optional
        The port number for UCMDB server. Defaults to 8443.
        Common ports: 443 (containerized), 8443 (traditional), 9443.

    Returns
    -------
    dict
        Returns a dictionary object with the content-type of
        application/json and the authorization with the bearer
        token.

    Raises
    ------
    SystemExit
        If the user is not authorized, prints a message with the text
        of the rejection and exits the system.
    """
    r = authenticate(uduser, udpass, udsystem, port=port)
    data = r.json()
    if r.status_code == 200:
        token_data = 'Bearer ' + data['token']
        headers = {
            'Content-Type': 'application/json',
            'Authorization': token_data
        }
        return headers
    else:
        print(
            'Your user is not authorized. See the error below and contact '
            'your administrator'
        )
        print(r.text)
        sys.exit()



def getLicenseReport(token, udserver):
    """
    Retrieves the UCMDB license report from UCMDB.

    This method makes a GET request to the UCMDB server to fetch license
    information.

    Minimum UCMDB Version: 2023.05
    Note: Decorator not applied (defined later in this file)

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 'createHeaders'
        with arguments of ucmdb_user, ucmdb_pass, and ucmdb_server.
    udserver : str
        The UCMDB server hostname or IP address that is valid for DNS
        resolution.

    Returns
    -------
    requests.Response
        Can be converted to a dictionary with license information. For example:
        {
            "fullServerCount": 693,
            "fullWorkstationCount": 3,
            "fullNetworkCount": 0,
            "fullStorageCount": 0,
            "fullDockerCount": 0,
            "basicServerCount": 12,
            "basicWorkstationCount": 1,
            "basicNetworkCount": 0,
            "basicStorageCount": 0,
            "basicDockerCount": 0,
            "operationalServerCount": 0,
            "operationalWorkstationCount": 0,
            "operationalNetworkCount": 0,
            "operationalStorageCount": 0,
            "operationalDockerCount": 0,
            "usedUnit": "694.6",
            "totalLicenseUnit": 1000,
            "totalMDR": 20,
            "usedMDR": 0,
            "totalCM": 0,
            "usedCM": 0,
            "totalPremium": 0,
            "totalAsset": 0,
            "consumedAsset": 0,
            "consumedPremium": 0,
            "usedManagement": 0,
            "usedPremium": 0,
            "usedAsset": 0,
            "customerID": 0,
            "consumedCIs": 0,
            "maxCIs": 0,
            "usedProbes": 0,
            "maxProbes": 0,
            "allowBuffer": 0.0,
            "remainingDays": 394,
            "licenseDetailsCollection": [
                {
                    "description": "UCMDB Third Party Integration per MDR",
                    "licenseType": "TERM",
                    "expirationDate": 1752191999000,
                    "startDate": 1712665737000,
                    "capacity": 20,
                    "remainingDaysUntilExpireTime": "394",
                    "customerLicenseFeatures": {
                        "10398": 20
                    },
                    "active": true,
                    "formatExpirationDate": "7/10/25 4:59 PM",
                    "formatStartDate": "4/9/24 5:28 AM"
                },
                {
                    "description": "Universal Discovery per Unit V2",
                    "licenseType": "TERM",
                    "expirationDate": 1752191999000,
                    "startDate": 1712665693000,
                    "capacity": 1000,
                    "remainingDaysUntilExpireTime": "394",
                    "customerLicenseFeatures": {
                        "100787": 1000,
                        "10831": 1
                    },
                    "active": true,
                    "formatExpirationDate": "7/10/25 4:59 PM",
                    "formatStartDate": "4/9/24 5:28 AM"
                }
            ],
            "operational": false,
            "saminventory": false,
            "ucmdbfoundation": true,
            "rationOfManagementToAsset": 20
        }
    """
    return requests.get(
        _url(udserver, '/uiserver/license/report'),
        headers=token,
        verify=config.get_verify_ssl()
    )


def getUCMDBVersion(token, udserver):
    """
    Retrieves the UCMDB version from the REST API endpoint for the UCMDB
    server dashboard.

    This method makes a GET request to the UCMDB server to fetch version
    information.

    Minimum UCMDB Version: 2023.05
    Note: Decorator not applied (defined later in this file)

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 'createHeaders'
        with arguments of ucmdb_user, ucmdb_pass, and ucmdb_server.
    udserver : str
        The UCMDB server hostname or IP address that is valid for DNS
        resolution.

    Returns
    -------
    requests.Response
        Can be converted to a dictionary with version information. For example:
        {
            "productName": "Universal CMDB",
            "serverBuildNumber": "232",
            "contentPackBuildNumber": "67",
            "contentPackVersion": "24.2",
            "fullServerVersion": "11.8.0"
        }
    """
    return requests.get(
        _url(udserver, '/v1/uiserver/dashboard/versions/getVersion'),
        headers=token,
        verify=config.get_verify_ssl()
    )


def ping(udserver, restrictToWriter=False, restrictToReader=False):
    """
    Tests connectivity to UCMDB.

    This method makes a GET request to the UCMDB server to show connection
    information.

    Minimum UCMDB Version: 2023.05
    Note: Decorator not applied (defined later in this file)

    Parameters
    ----------
    udserver : str
        The UCMDB server hostname or IP address that is valid for DNS
        resolution.
    restrictToWriter : bool, optional
        When set to True, only if the server is a writer will this return
        a valid status. Default is False.
    restrictToReader : bool, optional
        When set to True, only if the server is a reader will this return
        a valid status. Default is False.

    Returns
    -------
    requests.Response
        Can be converted to a dictionary with status information. For example:
        {
            "status": {
                "statusCode": 200,
                "reasonPhrase": "OK",
                "message": "FullyUp, is writer: true"
            }
        }
    """
    url = _url(
        udserver,
        '/ping?restrictToWriter=' + str(restrictToWriter) +
        '&restrictToReader=' + str(restrictToReader)
    )
    return requests.get(url, verify=config.get_verify_ssl())


def runMethod(method, *args, print_debug=True, **kwargs):
    """
    A helper method that runs any given rest method and returns the
    result.

    Parameters
    ----------
    method : function
        This is the name of the function being called.
    *args : tuple
        These are the by position arguments sent to the function.
    print_debug : bool, optional
        Should additional information be printed? The default is True.
    **kwargs : dict
        These are any keyword arguments sent to the function.

    Returns
    -------
    myVar : requests.response
        The formatted output of the requests library call.
    """
    # print('The flag print_debug is:', print_debug, 'Calling method:', method.__name__)
    myVar = method(*args, **kwargs)
    if print_debug:
        print('Ran', method.__name__, 'and got status:', myVar.status_code)
    if myVar.status_code == 200:
        if print_debug:
            print('Results:')
            print(myVar.text)
            print('JSON:')
            try:
                if print_debug:
                    print(json.dumps(myVar.json(), indent=4))
            except json.JSONDecodeError as e:
                if print_debug:
                    print("Error: Failed to decode JSON")
                    print("Exception message:", str(e))
    elif myVar.status_code == 204:
        if print_debug:
            print('Action successful')
    else:
        if print_debug:
            print("Got an error")
            print(myVar.text)
    return myVar

def strToBool(s):
    """
    Converts a string (true, True, Yes, YES, Yes) to bool True

    Parameters
    ----------
    s : str
        The string to convert.

    Raises
    ------
    ValueError
        Value is not expected e.g. not:
            True
            False
            Yes
            No
            1
            0
            (case doesn't matter)

    Returns
    -------
    bool
        The boolean value associated with the string.

    """
    if s.lower() in ['true','yes','1']:
        return True
    elif s.lower() in ['false','no','0']:
        return False
    else:
        raise ValueError(f'Cannot convert {s} to bool')

addCiPrompt = (
    "Please enter the CI in a string to create.\n"
    "Enter '1' to show an example of a valid CI string\n"
    "Use an empty string to accept a default value:"
)


# ============================================================================
# Version Checking Infrastructure
# ============================================================================

class UCMDBVersionError(Exception):
    """
    Exception raised when a function is called on a UCMDB version that
    doesn't support it.

    Attributes
    ----------
    message : str
        Explanation of the error including required and actual versions.
    """
    pass


# Global cache for UCMDB versions by server
_version_cache: Dict[str, str] = {}


def _normalize_version(version_str: str) -> tuple:
    """
    Normalizes a UCMDB version string to a comparable tuple.

    Handles both formats:
    - YYYY.MM format (e.g., "2023.05", "2023.08") - represents calendar year.month
    - YY.M format (e.g., "23.4", "24.2", "25.4") - represents release year.quarter

    UCMDB uses two different versioning schemes:
    - YYYY.MM: Calendar-based (2023.05 = May 2023, 2023.08 = Aug 2023)
    - YY.Q: Quarterly releases (23.4 = Q4 2023, 24.2 = Q2 2024)
      where Q1=Jan, Q2=Apr, Q3=Jul, Q4=Oct

    Parameters
    ----------
    version_str : str
        The version string to normalize.

    Returns
    -------
    tuple
        A tuple of (year, month_or_quarter, is_quarterly) for comparison.
        The third element distinguishes between the two formats.

    Examples
    --------
    >>> _normalize_version("2023.05")
    (2023, 5, False)
    >>> _normalize_version("23.4")
    (2023, 10, True)
    >>> _normalize_version("24.2")
    (2024, 4, True)
    """
    parts = version_str.split('.')
    year = int(parts[0])
    second_part = int(parts[1])

    # Determine if this is YYYY.MM or YY.Q format
    if year >= 1000:
        # YYYY.MM format (calendar-based)
        return (year, second_part, False)
    else:
        # YY.Q format (quarterly releases)
        # Convert YY to YYYY
        year += 2000

        # Convert quarter to month: Q1=1, Q2=4, Q3=7, Q4=10
        quarter_to_month = {1: 1, 2: 4, 3: 7, 4: 10}
        month = quarter_to_month.get(second_part, second_part)

        return (year, month, True)


def compare_versions(current: str, required: str) -> bool:
    """
    Compares two UCMDB version strings.

    Handles both UCMDB versioning schemes:
    - YYYY.MM (calendar-based): 2023.05 = May 2023, 2023.08 = Aug 2023
    - YY.Q (quarterly): 23.4 = Q4 2023 (Oct), 24.2 = Q2 2024 (Apr)

    Parameters
    ----------
    current : str
        The current UCMDB version (e.g., from getUCMDBVersion).
    required : str
        The required minimum version.

    Returns
    -------
    bool
        True if current >= required, False otherwise.

    Examples
    --------
    >>> compare_versions("24.2", "23.4")
    True
    >>> compare_versions("23.4", "24.2")
    False
    >>> compare_versions("23.4", "2023.05")  # Oct 2023 > May 2023
    True
    >>> compare_versions("2023.05", "23.4")  # May 2023 < Oct 2023
    False
    >>> compare_versions("24.2", "2023.05")  # Apr 2024 > May 2023
    True
    """
    current_tuple = _normalize_version(current)
    required_tuple = _normalize_version(required)
    return current_tuple >= required_tuple


def _get_cached_version(token: dict, udserver: str) -> str:
    """
    Retrieves the UCMDB version from cache or fetches it from the server.

    Parameters
    ----------
    token : dict
        Authentication token from createHeaders.
    udserver : str
        UCMDB server hostname or IP.

    Returns
    -------
    str
        The UCMDB version string (e.g., "24.2", "2023.05").
    """
    if udserver not in _version_cache:
        version_response = getUCMDBVersion(token, udserver)
        if version_response.status_code == 200:
            version_data = version_response.json()
            # Extract version - could be in different formats
            full_version = version_data.get('fullServerVersion', '')
            content_pack_version = version_data.get('contentPackVersion', '')

            # Use contentPackVersion as it matches the release format (e.g., "24.2")
            _version_cache[udserver] = content_pack_version if content_pack_version else full_version
        else:
            raise UCMDBVersionError(
                f"Failed to retrieve UCMDB version from {udserver}. "
                f"Status code: {version_response.status_code}"
            )

    return _version_cache[udserver]


def requires_version(min_version: str):
    """
    Decorator to enforce minimum UCMDB version requirements for API functions.

    This decorator checks if the UCMDB server version meets the minimum
    requirement before executing the function. If the version is too old,
    it raises a UCMDBVersionError.

    Parameters
    ----------
    min_version : str
        The minimum UCMDB version required (e.g., "24.2", "2023.05").

    Returns
    -------
    function
        The decorated function with version checking.

    Raises
    ------
    UCMDBVersionError
        If the UCMDB server version is older than the required version.

    Examples
    --------
    >>> @requires_version("24.2")
    ... def getPackages(token, udserver):
    ...     return requests.get(_url(udserver, '/packages'), headers=token)

    Notes
    -----
    - The decorated function MUST have 'token' and 'udserver' as the first
      two parameters (in that order).
    - Version information is cached per server to minimize API calls.
    - To bypass version checking for testing, users can clear the cache
      and mock getUCMDBVersion.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(token, udserver, *args, **kwargs):
            # Get the current UCMDB version (cached)
            try:
                current_version = _get_cached_version(token, udserver)
            except Exception as e:
                # If we can't get the version, log a warning but allow the call
                print(f"Warning: Could not verify UCMDB version: {e}")
                print("Proceeding with function call anyway...")
                return func(token, udserver, *args, **kwargs)

            # Compare versions
            if not compare_versions(current_version, min_version):
                raise UCMDBVersionError(
                    f"Function '{func.__name__}' requires UCMDB version {min_version} or later. "
                    f"Your UCMDB server ({udserver}) is running version {current_version}."
                )

            # Version check passed, execute the function
            return func(token, udserver, *args, **kwargs)

        return wrapper
    return decorator


def clear_version_cache():
    """
    Clears the global version cache.

    Useful for testing or when connecting to a server that has been upgraded.
    """
    global _version_cache
    _version_cache.clear()
