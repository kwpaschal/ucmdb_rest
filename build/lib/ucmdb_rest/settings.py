# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:26:41 2024

@author: kpaschal

This library contains methods use for settings and reipient manager
"""

import requests

from .utils import _url

def addRecipients(token, udserver, recipient_dict):
    """
    Updates a recipient with a display label and email address(es). Uses
    a POST call to the UCMDB REST API.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution
        (IP or hostname).
    recipient_dict : dict
        A dictionary containing recipient details. For example:
            {
                "id": "",
                "name": "Keith",
                "addresses": [
                    "kpaschal@opentext.com"
                ]
            }

    Returns
    -------
    requests.Response
        A list of dictionaries containing the user/email address(es).
        For example:
            [
                {
                    "name": "Keith",
                    "addresses": [
                        "kpaschal@mycompany.com"
                    ],
                    "id": "23005b6794db6c48eb18288ef0879194"
                }
            ]
    """
    return requests.post(_url(udserver, '/administration/recipients'), 
                         headers=token, json=recipient_dict, 
                         verify=False)

def deleteRecipients(token, udserver, id_to_delete):
    """
    This method deletes a user from the recipients manager via a
    DELETE call to the REST API in UCMDB.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution
        (IP or hostname).
    id_to_delete : str
        ID, which can be retrieved from a 'getRecipients' call.

    Returns
    -------
    requests.Response
        Exits with a 204 HTTP code... So nothing should be
        returned.

    """
    myUrl = _url(udserver, f'/administration/recipients?ids={id_to_delete}')
    return requests.delete(myUrl, headers=token, verify=False)

def getRecipients(token, udserver):
    """
    Gets a list of recipients from UCMDB via a REST API get call.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution
        (IP or hostname).

    Returns
    -------
    requests.Response
        A list of dictionaries with recipient details. For example:
            [
                {
                    "name": "Joe",
                    "addresses": [
                        "joe@mycompany.com"
                    ],
                    "id": "dc1942e4a816a0f5fe663d8gcg9222fd"
                },
                {
                    "name": "Keith",
                    "addresses": [
                        "keithpaschal@mycompany.com",
                        "kpaschal@mycompany.com"
                    ],
                    "id": "f72f7d7b61af053d0fa984360419e79e"
                }
            ]
    """
    return requests.get(_url(udserver, '/administration/recipients'), 
                        headers=token, verify=False)

def getSetting(token, udserver, setting, locale='en'):
    """
    Retrieves a setting from UCMDB.

    This function makes a GET request to the UCMDB server to 
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
    setting : str
        Setting to retrieve in the format shown in the UCMDB CMS UI.
        For example: multi.tenancy.global.default.tenant_id
    locale : str, optional
        Language to use. Supported locales are: da, de, el, en, es, fr,
        is, it, ja, ko, nb, nl, pl, pt_BR, pt_PT, ru, sv, tr, zh_CN.
        Default is 'en'.

    Returns
    -------
    requests.Response
        A dictionary object containing the details of the setting.
        Example:
        {
          "name": "multi.tenancy.global.default.tenant_id",
          "value": "System Default Tenant",
          "valueType": "STRING",
          "defaultValue": "System Default Tenant",
          "factoryValue": "System Default Tenant",
          "displayName": "Global MSPTenant",
          "description": "Global MSP Tenant id, this tenant will be 
                         created at start up if multitenancy enabled",
          "refreshRate": "Reboot",
          "displayInUI": false,
          "sectionName": "section.general",
          "sectionDisplayName": "General Settings",
          "scope": "GLOBAL",
          "editable": true,
          "displayType": "string"
        }
    """
    return requests.get(_url(udserver, '/settings/' + setting), 
                        headers=token, verify=False)

def setSetting(token, udserver, setting, body, locale='en'):
    """
    Sets a setting in UCMDB.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution
        (IP or hostname).
    setting : str
        Setting to retrieve in the format shown in the UCMDB CMS UI.
        For example: multi.tenancy.global.default.tenant_id.
    body : dict
        Contains the value to be set. For example:
            {
                "value": "myuser@opentext.com"
            }
    locale : str, optional
        Language to use. Supported locales are: da, de, el, en, es, fr,
        is, it, ja, ko, nb, nl, pl, pt_BR, pt_PT, ru, sv, tr, zh_CN.
        Default is 'en'.

    Returns
    -------
    requests.Response
        JSON values after the set is complete. For example:
            {
                "name": "email.send.from",
                "value": "myuser@opentext.com",
                "valueType": "STRING",
                "defaultValue": "admin@opentext.com",
                "factoryValue": "admin@ucmdb.com",
                "displayName": "settings.email.send.from.name.name",
                "description": "settings.email.send.from.name.desc",
                "refreshRate": "Login",
                "displayInUI": true,
                "sectionName": "section.mail",
                "sectionDisplayName": "section.mail",
                "scope": "CUSTOMER",
                "editable": true,
                "displayType": "email"
            }
    """
    return requests.put(_url(udserver, '/settings/' + setting), 
                        headers=token, json=body, verify=False)

def updateRecipients(token, udserver, id_to_update, dict_to_update):
    """
    This method updates a user from the recipients manager via a
    PUT call to the REST API in UCMDB.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution
        (IP or hostname).
    id_to_update : str
        ID, which can be retrieved from a 'getRecipients' call.
    dict_to_update : dict
        Dictionary containing the modification to be made, for
        example::

            {
                "name": "Keith",
                "addresses": [
                    "keithp@mycompany.com",
                    "kp@mycompany.com",
                    "kp@mycompany.org",
                    "kpaschal@mycompany.com"
                ],
                "id": "231f6bfe675f41225bc7dd87622ce82d"
            }

    Returns
    -------
    requests.Response
        Dictionary with the result of the update. For example::

            {
                "name": "Keith",
                "addresses": [
                    "keithp@mycompany.com",
                    "kp@mycompany.com",
                    "kp@mycompany.org",
                    "kpaschal@mycompany.com"
                ],
                "id": "231f6bfe675f41225bc7dd87622ce82d"
            }

    """
    myUrl = _url(udserver, f'/administration/recipients/{id_to_update}')
    return requests.put(myUrl, headers=token, json=dict_to_update, 
                        verify=False)