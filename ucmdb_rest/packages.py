# -*- coding: utf-8 -*-
"""
UCMDB Package and Content Pack Service

This module manages the deployment, export, and status of UCMDB packages 
and official Content Packs.

Package Operations:
    deletePackage, deployPackage, exportPackage, filterPackage, 
    getPackage, getPackages, getProgress

Content Pack Operations:
    getContentPacks, getSpecificContentPack, getDiffReport, uploadContentPack
"""

from urllib.parse import quote


class Packages:
    def __init__(self, client):
        """
        Initialize the service with a reference to the main level UCMDB client
        """
        self.client = client

    def deletePackage(self, package):
        """
        Delete a package from the UCMDB server.

        This function makes a DELETE request to the UCMDB server to undeploy
        a specified package.

        Parameters
        ----------
        package : str
            Package to undeploy.

        Returns
        -------
        requests.Response
            A dictionary of the result of the deletePackage call:
            {
            "failedResources": [],
            "successResources": [
                {
                "errorCode": {
                    "description": "",
                    "code": 0,
                    "errorParametersValues": null,
                    "parametrizedError": false
                },
                "resourceInfo": {
                    "subSystem": "discoveryPatterns",
                    "subSystemDisplayName": "",
                    "name": "KWPDisk",
                    "extension": "xml",
                    "path": "",
                    "packageName": "",
                    "packageDisplayName": "KWP",
                    "cmdbVersion": "",
                    "updateTime": 0,
                    "isFactory": false,
                    "data": null,
                    "recalculateName": true,
                    "absoluteName": "discoveryPatterns/KWPDisk.xml",
                    "qualifiedName": "",
                    "currentVersion": false,
                    "subSystemName": "discoveryPatterns",
                    "noVersionSet": true
                },
                "deploySuccessful": true
                }
            ]
            }
        """
        safe_package = quote(package)
        url = f'{self.client.base_url}/packagemanager/packages/{safe_package}'
        return self.client.session.delete(url)

    def deployPackage(self, filestoupload, package_name):
        """
        Deploy a package to the UCMDB server.

        This function makes a POST request to the UCMDB server to upload and
        deploy a specified package.

        Parameters
        ----------
        filestoupload : bytes
            Binary read of the file to upload.
        package_name : str
            Name of the package to associate with these files.

        Returns
        -------
        requests.Response
            A dictionary of the result of the deployPackage call:
            {
            "failedResources": [],
            "successResources": [
                {
                "errorCode": {
                    "description": "",
                    "code": 0,
                    "errorParametersValues": null,
                    "parametrizedError": false
                },
                "resourceInfo": {
                    "subSystem": "discoveryPatterns",
                    "subSystemDisplayName": "",
                    "name": "KWPDisk",
                    "extension": "xml",
                    "path": "",
                    "packageName": "",
                    "packageDisplayName": "KWP",
                    "cmdbVersion": "",
                    "updateTime": 0,
                    "isFactory": false,
                    "data": null,
                    "recalculateName": true,
                    "absoluteName": "discoveryPatterns/KWPDisk.xml",
                    "qualifiedName": "",
                    "currentVersion": false,
                    "subSystemName": "discoveryPatterns",
                    "noVersionSet": true
                },
                "deploySuccessful": true
                },
                ...
            ]
            }
        """
        files_uploaded = {
            'file': (package_name, filestoupload),
            'type': 'application/x-zip-compressed'
        }
        url = f'{self.client.base_url}/packagemanager/packages'
        return self.client.session.post(url,files=files_uploaded)

    def exportPackage(self, package_name):
        """
        Export a package from the UCMDB server.

        This function makes a GET request to the UCMDB server to export a
        specified package.

        Parameters
        ----------
        package_name : str
            Package name to sync (zip file name).

        Returns
        -------
        bytes
            Binary file to be written.
        """
        safe_package = quote(package_name)
        url = f'{self.client.base_url}/uiserver/packagemanager/resources/export?packageName={safe_package}'  # noqa: E501
        return self.client.session.get(url)

    def filterPackage(self, package):
        """
        Filter a package from the UCMDB server.

        This function makes a GET request to the UCMDB server to list the
        specified package.

        Parameters
        ----------
        package : str
            Package name to list (should be the displayName of the package).

        Returns
        -------
        requests.Response
            A dictionary containing all information about the package name:
            {
                "collection": [
                    {
                        "name": "KWP.zip",
                        "displayName": "KWP",
                        "lastModifiedTime": 1718134976552,
                        "dependencies": [],
                        "version": "2019.05",
                        "category": "UCMDB",
                        "description": "This package contains the information
                                        needed to discover disks and their size.",
                        "updatedBy": "admin",
                        "updatedVersion": 3,
                        "buildNumber": "",
                        "minVersion": "",
                        "maxVersion": "",
                        "operationErrorCode": 0,
                        "readme": "",
                        "undeployResources": null,
                        "subSystems": [
                            "discoveryJobs",
                            "discoveryScripts",
                            "discoveryPatterns"
                        ],
                        "errorCode": 0,
                        "hidden": false,
                        "allResources": [
                            {
                                "subSystem":"discoveryJobs",
                                ...
                            }
                        ]
                    }
                ]
            }
        """
        safe_package = quote(package)
        url = f'{self.client.base_url}/uiserver/packagemanager/packages?isPaginationEnabled=true&start=0&limit=20&sortDir=ASC&sortField=name&search={safe_package}'  # noqa: E501
        return self.client.session.get(url)

    def getContentPacks(self):
        """
        Get the content packs from the UCMDB server.

        This function makes a GET request to the UCMDB server to retrieve
        information about the deployed content packs.

        Parameters
        ----------
        None

        Returns
        -------
        requests.Response
            List of content pack information:
            [
                {
                    "version": "23.4.198",
                    "cpStatus": "DEPLOYED",
                    "incompliantClasses": null,
                    "cpDeploymentProgress": "",
                    "cpDeploymentPercentage": ""
                },
                {
                    "version": "24.1.109",
                    "cpStatus": "UPLOADED",
                    "incompliantClasses": null,
                    "cpDeploymentProgress": "",
                    "cpDeploymentPercentage": ""
                },
                {
                    "version": "24.2.67",
                    "cpStatus": "UPLOADED",
                    "incompliantClasses": null,
                    "cpDeploymentProgress": "",
                    "cpDeploymentPercentage": ""
                }
            ]
        """
        url = f'{self.client.base_url}/packagemanager/contentpacks'
        return self.client.session.get(url)

    def getDiffReport(self, cpversion):
        """
        Retrieve the difference report for a content pack version.

        This function makes a GET request to the UCMDB server to 
        retrieve the difference report for a specified content pack 
        version.

        Parameters
        ----------
        cpversion : str
            Content Pack Version.

        Returns
        -------
        requests.Response
            JSON output with Difference Report if error, otherwise 
            binary file with report.
        """
        url = f'{self.client.base_url}/packagemanager/contentpacks/{cpversion}/diffreport'
        return self.client.session.get(url)

    def getPackage(self, pkg_name='A10_vthunder.zip'):
        """
        Retrieves details of a specific package from the UCMDB server.

        This method makes a GET request to the UCMDB server to retrieve details of
        the specified package.

        Parameters
        ----------
        pkg_name : str, optional
            Name of the package to retrieve. Defaults to 'A10_vthunder.zip'.

        Returns
        -------
        requests.Response
            Response object containing a JSON listing of the package details,
            including name, display name, version, and a list of resources it
            contains.

        """
        safe_package = quote(pkg_name)
        url = f'{self.client.base_url}/packagemanager/packages/{safe_package}'
        return self.client.session.get(url)

    def getPackages(self):
        """
        Retrieves a list of packages from the UCMDB server.

        This method makes a GET request to the UCMDB server to retrieve a list
        of packages.

        Parameters
        ----------
        None

        Returns
        -------
        requests.Response
            A list containing dictionaries with details of each package:
            - name: str
            - displayName: str
            - lastModifiedTime: int
            - dependencies: list of str
            - version: str
            - category: str
            - description: str
            - updatedBy: str
            - updatedVersion: int
            - buildNumber: str
            - minVersion: str
            - maxVersion: str
            - operationErrorCode: int
            - readme: str
            - undeployResources: None
            - factory: bool
            - hidden: bool
            - errorCode: int
            - allResources: list of dict, each containing details of a resource:
                - subSystem: str
                - subSystemDisplayName: str
                - name: str
                - extension: str
                - path: str
                - packageName: str
                - packageDisplayName: str
                - cmdbVersion: str
                - updateTime: int
                - isFactory: bool
                - data: str
                - recalculateName: bool
                - absoluteName: str
                - qualifiedName: str
                - currentVersion: bool
                - noVersionSet: bool
                - subSystemName: str

        """
        url = f'{self.client.base_url}/packagemanager/packages'
        return self.client.session.get(url)

    def getProgress(self, package):
        """
        Retrieves the deployment or undeployment progress for a specific package.

        Parameters
        ----------
        package : str
            Name of the package to check.

        Returns
        -------
        requests.Response
            A JSON response indicating status (e.g., 'FINISHED', 'IN_PROGRESS') 
            and any failed resource names.
        """
        safe_package = quote(package)
        url = f'{self.client.base_url}/packagemanager/packages/{safe_package}/progress'
        return self.client.session.get(url)

    def getSpecificContentPack(self, cpversion):
        """
        Retrieves the status and deployment percentage of a specific Content Pack.

        Parameters
        ----------
        cpversion : str
            The version string of the Content Pack (e.g., '24.1.109').

        Returns
        -------
        requests.Response
            JSON containing deployment status and completion percentage.
            
            {
            "version": "24.1.109",
            "cpStatus": "SIMULATED_INSTALLATION_FINISHED",
            "incompliantClasses": null,
            "cpDeploymentProgress": "FINISHED",
            "cpDeploymentPercentage": "100%"
            }
        """
        url = f'{self.client.base_url}/packagemanager/contentpacks/{cpversion}'
        return self.client.session.get(url)

    def uploadContentPack(self, filestoupload, cp_name):
        """
        Uploads a new Content Pack version to the UCMDB server.

        Parameters
        ----------
        filestoupload : bytes
            Binary content of the Content Pack file.
        cp_name : str
            The name/version to associate with the upload.

        Returns
        -------
        requests.Response
            Status of the upload process.
                {
                "name" : null,
                "errorCode" : {
                    "description" : "CP was uploaded successfully",
                    "code" : 0,
                    "parametrizedError" : false,
                    "errorParametersValues" : null
                },
                "successResources" : [ ],
                "failedResources" : [ ],
                "deploySuccessful" : true,
                "resourcesStatus" : [ ]
                }
        """
        files_uploaded = {'file': (cp_name, filestoupload)}
        url = f'{self.client.base_url}/packagemanager/contentpacks'
        return self.client.session.post(url,files=files_uploaded)