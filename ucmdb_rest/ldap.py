# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:05:36 2024

@author: kpaschal

This python library contains methods dealing with LDAP settings in the 
UCMDB server.
"""

import requests

from .utils import _url
from . import config

def getLDAPSettings(token, udserver):
    """
    Retrieves the LDAP configuration from UCMDB.

    This function makes a GET request to the UCMDB server to retrieve
    the information.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, and
        ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution (IP or
        hostname).

    Returns
    -------
    requests.Response
        A list of dictionaries containing 1 LDAP entry per list entry.
        
        Example
        -------
        [
            {
                "connection": {
                    "url": "ldap://ftcdc02.swinfra.net:389/OU=2-Resources,DC=swinfra,DC=net??sub",
                    "searchUser": "CN=_UCMDBLDAP (00330644),OU=Missouri,OU=Americas,OU=2.2.1-Service Accounts - Std,OU=2-Resources,DC=swinfra,DC=net",
                    "searchUserPassword": null,
                    "enabledSearchForDN": true
                },
                "group": {
                    "groupSearch": {
                        "base": "OU=_Other,OU=Americas,OU=2.5.1-Groups - Std,OU=2-Resources,DC=swinfra,DC=net",
                        "filter": "(&(objectclass=group)(cn=sec-gg-ucmdb*))",
                        "scope": "sub"
                    },
                    "rootGroupSearch": {
                        "base": "OU=_Other,OU=Americas,OU=2.5.1-Groups - Std,OU=2-Resources,DC=swinfra,DC=net",
                        "filter": "(&(objectclass=group)(cn=sec-gg-ucmdb*))",
                        "scope": "sub"
                    },
                    "useBottomUpAlgorithm": true
                },
                "staticGroup": {
                    "groupClass": "group",
                    "nameAttribute": "cn",
                    "descriptionAttribute": "description",
                    "displayNameAttribute": "cn",
                    "memberAttribute": "member"
                },
                "dynamicGroup": {
                    "enabled": false,
                    "groupClass": null,
                    "descriptionAttribute": null,
                    "displayNameAttribute": null,
                    "memberAttribute": null,
                    "nameAttribute": null
                },
                "user": {
                    "userClass": "user",
                    "displayNameAttribute": "cn",
                    "uniqueIdAttribute": "employeeID",
                    "userFilter": "(&(employeeID=*)(objectClass=user))",
                    "displayUsersGroup": true,
                    "splitRepositoryFromLoginName": true,
                    "userSearch": {
                        "base": null,
                        "filter": null,
                        "scope": null,
                        "nrOfUsersRetrievedAtOnce": 20,
                        "distinguishedNameAttribute": ""
                    }
                },
                "integration": {
                    "defaultGroup": "UCMDBAdmins",
                    "priority": 2
                }
            }
        ]
    """
    return requests.get(_url(udserver, '/ldap/settings'), headers=token, verify=config.get_verify_ssl())