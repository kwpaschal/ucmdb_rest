# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:12:48 2024

@author: kpaschal

This python library contains methods dealing with managment zones in the 
UCMDB server.  These zones are CMS UI zones, not UCMDB local client 
management zones.
"""

import requests

from .utils import _url

def activateZone(token, udserver, zone_id):
    """
    Activates a management zone on the UCMDB server.

    This method makes a PATCH request to the UCMDB server to activate a specific
    management zone.

    Parameters:
    -----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    zone_id : str
        The ID of the management zone to activate.

    Returns:
    --------
    requests.Response
        Response object confirming the activation of the management zone.

    Example:
    --------
    >>> token = 'example_token'
    >>> udserver = 'example_ucmdb_server'
    >>> zone_id = 'example_zone_id'
    >>> response = activateZone(token, udserver, zone_id)
    >>> print(response.status_code)
    200
    """
    return requests.patch(_url(udserver, '/discovery/managementzones/' + zone_id +
                               '?operation=activate'), headers=token, verify=False)

def createManagementZone(token, udserver, mgmtZone):
    """
    Creates a new management zone on the UCMDB server.

    This method makes a POST request to the UCMDB server to create a 
    new management zone.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    mgmtZone : dict
        Dictionary containing the details of the management zone to be 
        created.
        Example:
        {
            "name": "Zone Via REST-API",
            "activated": False,
            "ipRangeProfiles": [
                {
                    "ipRangeProfileId": "All IP Range Groups"
                }
            ],
            "discoveryActivities": [
                {
                    "discoveryProfileId": "Added Thru REST-API",
                    "scheduleProfileId": "Interval 1 Day (Default)",
                    "credentialProfileId": "All Credentials"
                }
            ]
        }

    Returns
    -------
    requests.Response
        Response object confirming the creation of the management zone.

    Example
    -------
    >>> token = 'example_token'
    >>> udserver = 'example_ucmdb_server'
    >>> mgmtZone = {
    >>>     "name": "Zone Via REST-API",
    >>>     "activated": False,
    >>>     "ipRangeProfiles": [
    >>>         {
    >>>             "ipRangeProfileId": "All IP Range Groups"
    >>>         }
    >>>     ],
    >>>     "discoveryActivities": [
    >>>         {
    >>>             "discoveryProfileId": "Added Thru REST-API",
    >>>             "scheduleProfileId": "Interval 1 Day (Default)",
    >>>             "credentialProfileId": "All Credentials"
    >>>         }
    >>>     ]
    >>> }
    >>> response = createManagementZone(token, udserver, mgmtZone)
    >>> print(response.status_code)
    >>> 200
    """
    return requests.post(
        _url(udserver, 'discovery/managementzones'),
        headers=token, 
        json=mgmtZone, 
        verify=False
    )

def deleteManagementZone(token, udserver, zone_id):
    """
    Deletes a management zone from the UCMDB server.

    This method makes a DELETE request to the UCMDB server to delete a specific
    management zone.

    Parameters:
    -----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    zone_id : str
        The ID of the management zone to delete.

    Returns:
    --------
    requests.Response
        Response object confirming the deletion of the management zone.

    Example:
    --------
    >>> token = 'example_token'
    >>> udserver = 'example_ucmdb_server'
    >>> zone_id = 'example_zone_id'
    >>> response = deleteManagementZone(token, udserver, zone_id)
    >>> print(response.status_code)
    200
    """
    return requests.delete(_url(udserver, '/discovery/managementzones/' + zone_id),
                           headers=token, verify=False)

def getMgmtZone(token, udserver):
    """
    Retrieves management zone details from the UCMDB server.

    This method makes a GET request to the UCMDB server to retrieve management
    zone details.

    Parameters:
    -----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.

    Returns:
    --------
    requests.Response
        The response contains a dictionary of items, the items are a list of
        dictionaries including:
            - name : String - The name of the management zone
            - activated :  Boolean - Is the zone active?
            - ipRangeProfiles : A list of dictionaries containing the id
            - discoveryActivities : A list of dictionaries with:
                - discoveryProfileId : String - Name of the acitivity
                - scheduleProfileId : String - Name of the interval
                - credentialProfileId : String - Name of the credentials
            - id : String - Zone name
            - description : String - Description of the discovery
            - triggerSummary : Dictionary - A list of trigger statuses
            
    Example:
    --------
    >>> token = 'example_token'
    >>> udserver = 'example_ucmdb_server'
    >>> response = getMgmtZone(token, udserver)
    >>> for key in response:
    >>>        for item in range(len(response[key])):
    >>>            for akey in response[key][item]:
    >>>                if akey == 'id':
    >>>                    list_of_zones.append(response[key][item][akey])
    >>> print('Zones available on this server')
    >>> print('==============================')
    >>> for item in range(len(list_of_zones)):
    >>>     print (list_of_zones[item])

    """
    return requests.get(_url(udserver, '/discovery/managementzones'),
                        headers=token, verify=False)


def getSpecificMgmtZone(token, udserver, zone_id):
    """
    Retrieves a specific management zone from the UCMDB server.

    This method makes a GET request to the UCMDB server to retrieve a specific
    management zone.

    Parameters:
    -----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    zone_id : str
        The ID of the management zone to retrieve.

    Returns:
    --------
    requests.Response
        The return is a list of dictionaries with a single entry, 'items'
        Items contains a list of dictionaries
            - name : str
            - Activated: bool
            - IP Range Profiles: list of dicts
            - Discovery Activities: list of dicts
                - Discovery Profile: str
                - Schedule Profile: str
                - Credential Profile: str
            - ID: str
            - Trigger Summary: dict
                - Total Count: int
                - Pending Count: int
                - In Progress Count: int
                - Success Count: int
                - Warning Count: int
                - Error Count: int
            - Result CI Count: int
            - Active Jobs: dict
                - ASMish: list of str

    Example:
    --------
    >>> token = 'example_token'
    >>> udserver = 'example_ucmdb_server'
    >>> zone_id = 'example_zone_id'
    >>> response = getSpecificMgmtZone(token, udserver, zone_id)
    >>> for key in myJson:
    >>>        if key=='activated':
    >>>            print (zone_to_get,'activated?:',myJson[key])
                
    """
    return requests.get(_url(udserver, '/discovery/managementzones/' + zone_id),
                        headers=token, verify=False)

def getStatisticsForZone(token, udserver, zone_id):
    """
    Retrieves statistics for a specific management zone from the UCMDB server.

    This method makes a GET request to the UCMDB server to retrieve statistics
    for a specific management zone.

    Parameters:
    -----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    zone_id : str
        The ID of the management zone for which statistics are requested.

    Returns:
    --------
    requests.Response
        Response object containing the statistics for the specified management zone.

    Example:
    --------
    >>> token = 'example_token'
    >>> udserver = 'example_ucmdb_server'
    >>> zone_id = 'example_zone_id'
    >>> response = getStatisticsForZone(token, udserver, zone_id)
    >>> print(response.status_code)
    >>> 200
    """
    return requests.get(_url(udserver, '/discovery/results/statistics' + '?mzoneId=' + zone_id),
                        headers=token, verify=False)