# -*- coding: utf-8 -*-
"""
UCMDB System and Utility Service

This module provides methods for system-level health checks, connectivity 
verification, and licensing audits. It is essential for monitoring server 
availability and tracking resource consumption.

Exposed Methods:
    getLicenseInfo, getUCMDBVersion, ping
"""

class System:
    def __init__(self, server):
        """
        Initialize the service with a reference to the main level UCMDB server
        """
        self.server = server
    
    def getUCMDBVersion(self):
        """
        Retrieves the UCMDB version from the REST API endpoint for the UCMDB
        server dashboard.

        This method makes a GET request to the UCMDB server to fetch version
        information.

        This method is called automatically during UCMDBServer initialization 
        to populate the 'self.version' attribute for API compatibility checks.

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
        url = '/v1/uiserver/dashboard/versions/getVersion'
        return self.server._request("GET",url)

    def ping(self, restrictToWriter=False, restrictToReader=False):
        """
        Tests connectivity to UCMDB.

        This method makes a GET request to the UCMDB server to show connection
        information.

        Parameters
        ----------
        restrictToWriter : bool, optional
            If True, the ping only succeeds if the node is the primary 
            'Writer' node in a cluster. Default is False.
        restrictToReader : bool, optional
            If True, the ping only succeeds if the node is a 'Reader' node. 
            Default is False.

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
        url = f'{self.server.root_url}/ping?restrictToWriter={restrictToWriter}&restrictToReader={restrictToReader}'  # noqa: E501
        return self.server._request("GET",url)

    def getLicenseReport(self):
        """
        Retrieves detailed licensing and capacity information.

        This report includes license types (TERM/PERPETUAL), capacity limits, 
        remaining days until expiration, and active features for both 
        UCMDB and Universal Discovery.

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
        url = '/uiserver/license/report'
        return self.server._request("GET",url)