# -*- coding: utf-8 -*-
"""
UCMDB Integrations Service

This module provides methods for managing and monitoring UCMDB Integration Points. 
It supports both Data Population (pulling data into UCMDB) and Data Push 
(sending data to external systems).

Exposed Methods:
    getIntegrationDetails, getIntegrationInfo
"""
from urllib.parse import quote


class Integrations:
    def __init__(self, server):
        """
        Initialize the service with a reference to the main level UCMDB server
        """
        self.server = server

    def getIntegrationDetails(self, integrationpoint, detail=False):
        """
        Retrieves information about a specific integration point.

        This function makes a GET request to the UCMDB server to 
        retrieve information about a specific integration point.

        Parameters
        ----------
        integrationpoint : str
            An integration point name to get the details from.
        detail : bool
            This returns either verbose or non-verbose information. Must
            be set to True or False.

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
        safe_ip_name = quote(integrationpoint)
        detail_str = str(detail).lower()
        url = f'/integration/integrationpoints/{safe_ip_name}?detail={detail_str}'
        return self.server._request("GET",url)

    def getIntegrationInfo(self):
        """
        Retrieves information about integration points.

        This function makes a GET request to the UCMDB server to 
        retrieve information about integration points.

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
        url = '/integration/integrationpoints'
        return self.server._request("GET",url)