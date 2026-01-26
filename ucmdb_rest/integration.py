# -*- coding: utf-8 -*-
"""
UCMDB Integrations Service

This module provides methods for managing and monitoring UCMDB Integration Points. 
It supports both Data Population (pulling data into UCMDB) and Data Push 
(sending data to external systems).

Exposed Methods:
    getIntegrationDetails, getIntegrationInfo, clear_cache
"""
from urllib.parse import quote


class Integrations:
    def __init__(self, server):
        """
        Initialize the service with a reference to the main level UCMDB server
        """
        self.server = server

    def clear_cache(self, job_details):
        """
        This function clears the integration cache for a specific job (or jobs)
        inside a specific integration point

        Parameters
        ----------
        job_details : dict
            This is a dictionary which contains the integration point and which 
            jobs are to be cleared.  Use the getIntegrationDetails to retrieve
            the Integration Name and the Job names.  For example:
            {"IntegrationName":["JobName1","JobName2"]}
        
        Returns
        -------
        Request.response
          A Requests response containing the return status code of the clear
          or some text with an error message
        """
        url = '/integration/jobs'
        params = {'operation':'clearcache'}
        return self.server._request("PATCH", url, params=params, json=job_details)

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
    def setEnabledState(self, integration_id, enabled=True):
        """
        This method will either enable or disable a given integration point.
        
        Parameters
        ----------
        integration_id : str
            An integration point name.
        enabled : bool
            This is to enable (True) or Disable (False) the integration point.

        Returns
        -------
        requests.Response
            A dictionary object containing the details of a specific 
            integration point.
            for Example:
              {
                "errorCode": 200,
                "errorSource": null,
                "message": {
                  "code": 2200,
                  "parameter": null,
                  "description": null,
                  "errorParametersValues": [
                    "Test_Excel_import"
                  ],
                  "errorMap": null,
                  "parametrizedError": true
                },
                "details": null,
                "recommendedActions": null,
                "nestedErrors": null,
                "data": null
              }
        """
        url = f'/integration/integrationpoints/{integration_id}'
        params = {'enabled':enabled}
        return self.server._request("PATCH", url, params=params)
    
    def syncIntegrationPointJob(self, integration_id, job_id, operationtype="population_full"):
        """
        This function will run a synchronization of a current job under an integration 
        point.  It can run population_full, population_delta, push_full or push_delta

        Parameters
        ----------
        integration_id : str
            An integration point name.
        job_id : str
            The name of the job to run the action on
        operationtype : str
            The operations, restricted to this list: population_full, population_delta, push_full
            or push_delta

        Returns
        -------
        requests.Response
            A dictionary object containing the results of the operation on the job inside the
            integration point.
            For Example:
            {
              "errorCode": 200,
              "errorSource": null,
              "message": {
                "code": 13200,
                "parameter": null,
                "description": null,
                "errorParametersValues": [
                  "POPULATION_DELTA"
                ],
                "errorMap": null,
                "parametrizedError": true
              },
              "details": null,
              "recommendedActions": null,
              "nestedErrors": null,
              "data": null
            }
        """
        params = {'operationtype':operationtype}
        job_id = quote(job_id)
        url = f'/integration/integrationpoints/{integration_id}/jobs/{job_id}'
        return self.server._request("PATCH",url, params=params)
