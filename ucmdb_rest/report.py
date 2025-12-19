# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:10:48 2024

@author: kpaschal

This python library contains methods dealing with reports in the 
UCMDB server.
"""

from urllib.parse import quote

import requests

from .utils import _url

def changeReportsAll(token, udserver, toTime, fromTime, view):
    """
    Retrieves change reports for all elements within a specified time range
    and view.

    This method generates a request to retrieve change reports for all
    elements within a specified time range and view.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 'createHeaders'
        with arguments of ucmdb_user, ucmdb_pass, and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    toTime : str
        The end time of the time range for the report. Format is epoch time
        in milliseconds.
    fromTime : str
        The start time of the time range for the report. Format is epoch time
        in milliseconds.
    view : str
        The name of the view for which the change reports are requested.

    Returns
    -------
    requests.Response
        Response object containing the change reports.

    Example
    -------
    >>> token = 'example_token'
    >>> udserver = 'example_ucmdb_server'
    >>> toTime = '2024-05-30T00:00:00'
    >>> fromTime = '2024-05-01T00:00:00'
    >>> view = 'example_view'
    >>> response = changeReportsAll(token, udserver, toTime, fromTime, view)
    >>> print(response.status_code)
    >>> 200
    """
    body_json = {
        'dateFrom': str(fromTime),
        'dateTo': str(toTime),
        'viewName': view,
        'attributes': ['os_installed_date']
    }
    viewName = quote(view)
    encoded_filter = quote('type=ALL&attributes=description,name')
    the_url = _url(udserver, '/report/change/view/' + viewName + '/results?filter=' +
                   encoded_filter + '&dateFrom=' + str(fromTime) + '&dateTo=' + str(toTime) +
                   '&start=1&pageSize=100')
    #print('URL is:', the_url)
    return requests.get(the_url, headers=token, verify=False)

def changeReportsBlacklist(token, udserver, toTime, fromTime, view):
    """
    Retrieves a blacklist report for CIs in a view.

    This function makes a POST request to the UCMDB server to 
    retrieve the information.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution 
        (IP or hostname).
    toTime : int
        Time the report should end. Format is epoch time
        in milliseconds.
    fromTime : int
        Time the report should start. Format is epoch time
        in milliseconds.
    view : str
        Name of the view to retrieve the report from.

    Returns
    -------
    requests.Response
        A dictionary object containing the details of which attribute 
        changed, the date it was changed, and the old and new values. 
        Example:
        {
            "changes": {
                "4278e81d3dd6640a835e419d2865905d": {
                    "ciId": "4278e81d3dd6640a835e419d2865905d",
                    "displayLabel": "create222",
                    "className": "node",
                    "properties": [
                        {
                            "name": "Display Label",
                            "value": "USER LABEL"
                        },
                        {
                            "name": "Create Time",
                            "value": "Fri Jan 20 14:13:40 EET 2017"
                        },
                        {
                            "name": "Description",
                            "value": "description"
                        }
                    ],
                    "changes": {
                        "name": [
                            {
                                "attribute": "name",
                                "oldValue": "create2",
                                "newValue": "create22",
                                "changer": "User:{UISysadmin###UCMDB},LoggedInUser:{admin###UCMDB}",
                                "changeDate": 1484741091500
                            }
                        ]
                    }
                }
            }
        }
    """
    body_json = {
        'dateFrom': str(fromTime),
        'dateTo': str(toTime),
        'viewName': view,
        'attributes': ['description']
    }
    # TODO: Add 'description' as a variable to get a list of strings
    return requests.post(
        _url(udserver, '/changeReports/generate/blacklist'),
        headers=token,
        json=body_json,
        verify=False
    )

def changeReportsWhitelist(token, udserver, toTime, fromTime, view): 
    """
    Retrieves a whitelist report for CIs in a view.

    This function makes a POST request to the UCMDB server to 
    retrieve the information.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution 
        (IP or hostname).
    toTime : int
        Time the report should end, in the format: 1454364000000.
    fromTime : int
        Time the report should start, in the format: 1485986400000.
    view : str
        Name of the view to retrieve the report from.

    Returns
    -------
    requests.Response
        A dictionary object containing the details of which 
        attribute changed, the date it was changed, and the old and 
        new values. Example:
        {
            "changes": {
                "4278e81d3dd6640a835e419d2865905d": {
                    "ciId": "4278e81d3dd6640a835e419d2865905d",
                    "displayLabel": "create222",
                    "className": "node",
                    "properties": [
                        {
                            "name": "Display Label",
                            "value": "USER LABEL"
                        },
                        {
                            "name": "Create Time",
                            "value": "Fri Jan 20 14:13:40 EET 2017"
                        },
                        {
                            "name": "Description",
                            "value": "description"
                        }
                    ],
                    "changes": {
                        "name": [
                            {
                                "attribute": "name",
                                "oldValue": "create2",
                                "newValue": "create22",
                                "changer": "User:{UISysadmin###UCMDB},LoggedInUser:{admin###UCMDB}",
                                "changeDate": 1484741091500
                            }
                        ]
                    }
                }
            }
        }
    """
    # TODO: Make attributes a list of strings
    body_json = {
        'dateFrom': str(fromTime),
        'dateTo': str(toTime),
        'viewName': view,
        'attributes': ['name', 'primary_dns_name', 'data_note']
    }
    return requests.post(
        _url(udserver, '/changeReports/generate/whitelist'),
        headers=token,
        json=body_json,
        verify=False
    )