"""
Created on Mon Jun  3 16:45:23 2024

@author: kpaschal

This python library contains methods dealing with packages in the 
UCMDB server.
"""

import requests

from .utils import _url, requires_version

def deletePackage(ucmdb_server, token, package):
    """
    Delete a package from the UCMDB server.

    This function makes a DELETE request to the UCMDB server to undeploy
    a specified package.

    Parameters
    ----------
    ucmdb_server : str
        UCMDB Server to connect to.
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
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
    return requests.delete(
        _url(ucmdb_server, '/packagemanager/packages/' + package),
        headers=token,
        verify=False
    )


def deployPackage(ucmdb_server, token, filestoupload, package_name):
    """
    Deploy a package to the UCMDB server.

    This function makes a POST request to the UCMDB server to upload and
    deploy a specified package.

    Parameters
    ----------
    ucmdb_server : str
        UCMDB Server to connect to.
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
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
    return requests.post(
        _url(ucmdb_server, '/packagemanager/packages'),
        files=files_uploaded,
        headers=token,
        verify=False
    )

def exportPackage(ucmdb_server, token, package_name):
    """
    Export a package from the UCMDB server.

    This function makes a GET request to the UCMDB server to export a
    specified package.

    Parameters
    ----------
    ucmdb_server : str
        UCMDB Server to connect to.
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    package_name : str
        Package name to sync (zip file name).

    Returns
    -------
    bytes
        Binary file to be written.
    """
    myUrl = _url(
        ucmdb_server,
        '/uiserver/packagemanager/resources/export?packageName=',
        package_name
    )
    return requests.get(myUrl, headers=token, verify=False)

def filterPackage(ucmdb_server, token, package):
    """
    Filter a package from the UCMDB server.

    This function makes a GET request to the UCMDB server to list the
    specified package.

    Parameters
    ----------
    ucmdb_server : str
        UCMDB Server to connect to.
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
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
    myUrl = _url(
        ucmdb_server,
        '/uiserver/packagemanager/packages?isPaginationEnabled=true&start=0&limit=20&sortDir=ASC&sortField=name&search=',
        package,
        '&filter'
    )
    return requests.get(myUrl, headers=token, verify=False)

@requires_version("2023.05")
def getContentPacks(token, udserver):
    """
    Get the content packs from the UCMDB server.

    This function makes a GET request to the UCMDB server to retrieve
    information about the deployed content packs.

    Minimum UCMDB Version: 2023.05

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    udserver : str
        UCMDB Server to connect to.

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
    return requests.get(
        _url(udserver, '/packagemanager/contentpacks'),
        headers=token,
        verify=False
    )

def getDiffReport(ucmdb_server, token, cpversion):
    """
    Retrieve the difference report for a content pack version.

    This function makes a GET request to the UCMDB server to 
    retrieve the difference report for a specified content pack 
    version.

    Parameters
    ----------
    ucmdb_server : str
        UCMDB Server to connect to.
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    cpversion : str
        Content Pack Version.

    Returns
    -------
    requests.Response
        JSON output with Difference Report if error, otherwise 
        binary file with report.
    """
    return requests.get(
        _url(
            ucmdb_server,
            '/packagemanager/contentpacks/' + cpversion + '/diffreport'
        ),
        headers=token,
        verify=False
    )

def getPackage(token, udserver, pkg_name='A10_vthunder.zip'):
    """
    Retrieves details of a specific package from the UCMDB server.

    This method makes a GET request to the UCMDB server to retrieve details of
    the specified package.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 'createHeaders'
        with arguments of ucmdb_user, ucmdb_pass, and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address used to build the URL.
    pkg_name : str, optional
        Name of the package to retrieve. Defaults to 'A10_vthunder.zip'.

    Returns
    -------
    requests.Response
        Response object containing a JSON listing of the package details,
        including name, display name, version, and a list of resources it
        contains.

    Example
    -------
    >>> token = 'example_token'
    >>> udserver = 'example_ucmdb_server'
    >>> pkg_name = 'A10_vthunder.zip'
    >>> response = getPackage(token, udserver, pkg_name)
    >>> package_details = response.json()
    >>> print("Package Name:", package_details['name'])
    >>> print("Package Display Name:", package_details['displayName'])
    >>> print("Package Version:", package_details['version'])
    >>> print("Resources:")
    >>> for resource in package_details['allResources']:
    >>>     print("- Name:", resource['name'])
    >>>     print("  Subsystem:", resource['subSystem'])
    >>>     print("  Extension:", resource['extension'])
    >>>     print("  Path:", resource['path'])
    >>>     print("  CMDB Version:", resource['cmdbVersion'])
    >>>     print("  Last Modified Time:", resource['updateTime'])
    """
    return requests.get(_url(udserver, '/packagemanager/packages/' + pkg_name),
                        headers=token, verify=False)

@requires_version("2023.05")
def getPackages(token, udserver):
    """
    Retrieves a list of packages from the UCMDB server.

    This method makes a GET request to the UCMDB server to retrieve a list
    of packages.

    Minimum UCMDB Version: 2023.05

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 'createHeaders'
        with arguments of ucmdb_user, ucmdb_pass, and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address used to build the URL.

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
    return requests.get(_url(udserver, '/packagemanager/packages'),
                        headers=token, verify=False)

def getProgress(ucmdb_server, token, package):
    '''
    INPUT:
        ucmdb_server : str
            UCMDB Server to connect to
        token : dict
            Authentication token created by calling the function 
            'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
            and ucmdb_server.
        package : str
            Package to get status of
    RETURNS:
        requests.Response
        Dictionary with progress.  Example:
            {
                "status": "FINISHED",
                "detailMessage": null,
                "failedResourceNames": []
            }
    '''
    return requests.get(
        _url(ucmdb_server, 
             '/packagemanager/packages/' + package + '/progress'),
        headers=token, 
        verify=False
    )

def getSpecificContentPack(ucmdb_server, token, cpversion):
    '''
    INPUT:
        ucmdb_server : str
            UCMDB Server to connect to
        token : dict
            Authentication token created by calling the function 
            'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
            and ucmdb_server.
        cpversion : str
            Content Pack Version
    RETURNS:
        requests.Response
        JSON output with CP Version and status
        
        {
          "version": "24.1.109",
          "cpStatus": "SIMULATED_INSTALLATION_FINISHED",
          "incompliantClasses": null,
          "cpDeploymentProgress": "FINISHED",
          "cpDeploymentPercentage": "100%"
        }
    '''
    return requests.get(
        _url(ucmdb_server, 
             '/packagemanager/contentpacks/' + cpversion),
        headers=token, 
        verify=False
    )

def uploadContentPack(ucmdb_server, token, filestoupload, cp_name):
    '''
    INPUT:
        ucmdb_server : str
            UCMDB Server to connect to
        token : dict
            Authentication token created by calling the function 
            'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
            and ucmdb_server.
        filestoupload : Binary read file
        cp_name : str
            Name of the content pack (e.g. 24.1.109)
    RETURNS:
        requests.Response
            JSON with the status of the upload. For example:
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
    '''
    myUrl = _url(ucmdb_server, '/packagemanager/contentpacks')
    files_uploaded = {'file': (cp_name, filestoupload)}
    return requests.post(
        myUrl, 
        files=files_uploaded, 
        headers=token, 
        verify=False
    )



