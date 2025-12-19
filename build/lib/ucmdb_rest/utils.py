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


def authenticate(user, passwd, udserver, ssl=False):
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
    """
    payload = {
        'username': user,
        'password': passwd,
        'clientContext': '1'
    }
    try:
        return requests.post(_url(udserver, '/authenticate'), json=payload,
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


def createHeaders(uduser, udpass, udsystem):
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
    r = authenticate(uduser, udpass, udsystem)
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
        verify=False
    )


def getUCMDBVersion(token, udserver):
    """
    Retrieves the UCMDB version from the REST API endpoint for the UCMDB
    server dashboard.

    This method makes a GET request to the UCMDB server to fetch version
    information.

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
        verify=False
    )


def ping(udserver, restrictToWriter=False, restrictToReader=False):
    """
    Tests connectivity to UCMDB.

    This method makes a GET request to the UCMDB server to show connection
    information.

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
    return requests.get(url, verify=False)


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
