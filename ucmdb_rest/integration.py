# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:23:51 2024

@author: kpaschal

This python library contains methods dealing with integrations in the 
UCMDB server.
"""

import requests

from .utils import _url

def getIntegrationDetails(token, udserver, integrationpoint, detail ='false'):
    """
    Retrieves information about a specific integration point.

    This function makes a GET request to the UCMDB server to 
    retrieve information about a specific integration point.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution 
        (IP or hostname).
    integrationpoint : str
        An integration point name to get the details from.
    detail : str
        This returns either verbose or non-verbose information. Must
        be set to 'true' or 'false'.

    Returns
    -------
    requests.Response
        A dictionary object containing the details of a specific 
        integration point. Example (with true details):
        {
          "adapterCategory": "",
          "allProperties": {},
          "federationConfig": {
            "supportedCITs": [],
            "supportedAttributesForClasses": {},
            "selectedCITs": {},
            "selectedAttributesForClasses": {}
          },
          "populationConfig": {
            "supportedQueries": [],
            "supportedQueriesTree": {
              "name": "Root",
              "path": null,
              "children": [],
              "query": false,
              "folder": true
            },
            "jobs": [],
            "populationUsesQueries": true,
            "hasToHaveJob": false,
            "allowJob": false
          },
          "dataPushConfig": {
            "supportedQueries": [],
            "jobs": []
          },
          "supportChanges": false,
          "federationSupported": false,
          "populationSupported": false,
          "dataPushSupported": false,
          "remoteDeploySupported": false,
          "createMapforceFilesSupported": false,
          "resourcesLocator": false,
          "populationResourcesLocator": false,
          "pushResourcesLocator": false,
          "supportRepopulate": false,
          "selectedCIId": null,
          "dataStoreAdapterWrapper": {
            "adapterName": "ApiAdapter",
            "displayName": "UCMDB API Population",
            "description": "Allows defining Reconciliation Priority for API Data In flows",
            "category": "",
            "docName": "",
            "protocols": [],
            "supportChanges": false,
            "federationSupported": false,
            "populationSupported": false,
            "dataPushSupported": false,
            "remoteDeploySupported": false,
            "createMapforceFilesSupported": false,
            "resourcesLocator": false,
            "populationResourcesLocator": false,
            "pushResourcesLocator": false,
            "supportRepopulate": false,
            "isBaseOnTriggerCI": false,
            "allAdaptersProperties": {},
            "tqlNodeNames": null,
            "tql": null,
            "baseOnTriggerCI": false
          },
          "federationSelectedCIT": null,
          "name": "UCMDBDiscovery",
          "adapterName": "ApiAdapter",
          "description": null,
          "enabled": true
        }
    
    dict
        A dictionary object containing the details of a specific 
        integration point. Example (with false details):
        {
          "status": null,
          "successPopulationJob": -1,
          "errorPopulationJob": -1,
          "warningPopulationJob": -1,
          "totalPopulationJob": -1,
          "successPushJob": -1,
          "errorPushJob": -1,
          "warningPushJob": -1,
          "totalPushJob": -1,
          "allFederationSelectedCITs": 0,
          "federationSelectedCIT": "",
          "dataPopulationJobs": [],
          "dataPushJobs": [],
          "operationPushBlackItem": false,
          "serverSide": false,
          "basedOnTriggerCI": false,
          "name": "UCMDBDiscovery",
          "adapterName": "ApiAdapter",
          "description": null,
          "enabled": true
        }
    """
    return requests.get(
        _url(udserver, '/integration/integrationpoints/' +
             str(integrationpoint) + '?detail=' + detail),
        headers=token, 
        verify=False
    )

def getIntegrationInfo(token, udserver):
    """
    Retrieves information about integration points.

    This function makes a GET request to the UCMDB server to 
    retrieve information about integration points.

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
        A dictionary object containing the details of all 
        integration points. Example:
        {
          "HistoryDataSource": {
            "status": "SUCESSFULL",
            "successPopulationJob": 0,
            "errorPopulationJob": 0,
            "warningPopulationJob": 0,
            "totalPopulationJob": 0,
            "successPushJob": 0,
            "errorPushJob": 0,
            "warningPushJob": 0,
            "totalPushJob": 0,
            "allFederationSelectedCITs": 4,
            "federationSelectedCIT": null,
            "dataPopulationJobs": [],
            "dataPushJobs": [],
            "operationPushBlackItem": false,
            "serverSide": true,
            "basedOnTriggerCI": false,
            "name": "HistoryDataSource",
            "adapterName": "CmdbHistoryAdapter",
            "description": "",
            "enabled": true
          },
          "UCMDBDiscovery": {
            "status": "SUCESSFULL",
            "successPopulationJob": 0,
            "errorPopulationJob": 0,
            "warningPopulationJob": 0,
            "totalPopulationJob": 0,
            "successPushJob": 0,
            "errorPushJob": 0,
            "warningPushJob": 0,
            "totalPushJob": 0,
            "allFederationSelectedCITs": 0,
            "federationSelectedCIT": null,
            "dataPopulationJobs": [],
            "dataPushJobs": [],
            "operationPushBlackItem": false,
            "serverSide": true,
            "basedOnTriggerCI": false,
            "name": "UCMDBDiscovery",
            "adapterName": "ApiAdapter",
            "description": "",
            "enabled": true
          }
        }
    """
    return requests.get(
        _url(udserver, '/integration/integrationpoints'), 
        headers=token, 
        verify=False
    )
