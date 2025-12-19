# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:27:49 2024

@author: kpaschal
"""

import requests

from .utils import _url

def addRange(token, udserver, range_to_add, probe_name):
    """
    Creates a range in UCMDB for discovery.

    This function makes a POST request to the UCMDB server to create
    the range of IP Addresses.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, and
        ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution (IP or
        hostname).
    range_to_add : list of dict
        A list of dictionaries containing the range.
    probe_name : str
        The name of the probe to which the range is to be added.

    Returns
    -------
    requests.Response
    list of dicts
        A string representation of the created range.
        
        Example
        -------
        [
          {
            "range": "10.1.1.1-10.1.1.2",
            "definitionType": "IP_RANGE",
            "ipVersion": "IPV4",
            "isIncluded": true,
            "rangeType": "DATA_CENTER",
            "description": "My Range"
          }
        ]
    """
    return requests.post(_url(udserver, '/dataflowmanagement/probes/' +
                              probe_name + '/ranges'), headers=token,
                         json=range_to_add, verify=False)

def checkCredential (token, udserver, credential_id, probe, ip_addr,tout):
    """
    This function will check the credential from UCMDB server/Probe to a target

    Parameters
    ----------
    token : dict
        DESCRIPTION.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution (IP or
        hostname).
    credential_id : str
        The credential ID, like 3_1_CMS.
    probe: str
        Name of the probe
    ip_addr: str
        IP Address to run check agains
    tout: int
        Timeout in milliseconds

    Returns
    -------
    requests.Response
        The output of the agent communication.

    """
    timeout = int(tout) / 1000
    body_json = {
        'probeName':probe,
        'ipAddress':ip_addr,
        'timeout':tout
    }
    print()
    print('Please be patient for the configured timeout,',timeout,' seconds.')
    return requests.post(_url(udserver,'/dataflowmanagement/credentials/'+credential_id+'/availability'),headers=token, json=body_json, verify=False)

def createNTCMDCredential(token, udserver, my_protocol):
    """
    Creates an NTCMD credential in UCMDB.

    This function makes a POST request to the UCMDB server to create
    the credential.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, and
        ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution (IP or
        hostname).
    my_protocol : dict
        A dictionary containing the protocol.

    Returns
    -------
    requests.Response
        A string with the credential ID. For example:
        "10_1_CMS"
    """
    return requests.post(_url(udserver, '/dataflowmanagement/credentials'),
                         headers=token, json=my_protocol, verify=False)

def deleteProbe (token, udserver, probe_names):
    """
    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, and
        ucmdb_server.

    udserver : str
        UCMDB Server hostname that is valid from DNS resolution (IP or
        hostname).

    probe_names : list of strings
        A list of probes to delete.  For example:  ['probe1','probe2']

    Returns
    -------
    requests.Response
        Should be like an empty dictionary:
        For example:  {}

    """
    base_url = _url(udserver, '/dataflowmanagement/probes?')

    # Constructing the query parameters
    for i in range(len(probe_names)):
        if i == 0:
            base_url += f'probenames={probe_names[i]}'
        else:
            base_url += f'&probenames={probe_names[i]}'
    return requests.delete(base_url, headers=token, verify=False)

def deleteRange(token, udserver, delete_range, probe_name):
    """
    Deletes a range of IP Addresses in UCMDB for discovery.

    This function makes a DELETE request to the UCMDB server to
    create the range of IP Addresses.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution
        (IP or hostname).
    delete_range : list of dict
        A list of dictionaries containing the range. For example:
            [
              {
                "probe": "FTC06UCM43",
                "range": "10.1.1.1-10.1.1.2",
                "definitionType": "IP_RANGE",
                "ipVersion": "IPV4",
                "isIncluded": true
              }
            ]
    probe_name : str
        The name of the probe to which the range is to be added.

    Returns
    -------
     requests.Response
        Should be like an empty dictionary:
        For example:  {}
    """
    return requests.delete(
        _url(udserver, '/dataflowmanagement/probes/' + probe_name + '/ranges'),
        json=delete_range,
        headers=token,
        verify=False
    )


def do_availability_check(token, udserver, ci_to_check, probe):
    """
    Checks the availability of a given credential.

    This function makes a POST request to the UCMDB server to check the
    availability of the credential.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 'createHeaders'
        with arguments of ucmdb_user, ucmdb_pass, and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution (IP or
        hostname).
    ci_to_check : dict
        A dictionary of the UD Agent CI to check.
    probe : str
        The probe the CI is part of.

    Returns
    -------
    requests.Response
        Can be converted to a dictionary containing the results of the check.
    """
    json_body = {
        'probeName': probe,
        'ipAddress': ci_to_check['application_ip'],
        'timeout': 600000
    }
    url_to_run = '/dataflowmanagement/credentials/' + str(ci_to_check['credentials_id']) + '/availability'
    return requests.post(
        _url(udserver, url_to_run), 
        headers=token, 
        json=json_body, 
        verify=False
    )

def getAllDomains(token, udserver):
    """
    Retrieves the list of configured domains from UCMDB.

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
        Can be converted to a list of dictionaries containing 1 domain entry per list
        entry.
        
        Example
        -------
        [
          {
            "domainName": "DefaultDomain",
            "description": "",
            "credentialNum": "5",
            "probeNum": "1"
          }
        ]
    """
    return requests.get(_url(udserver, '/dataflowmanagement/domains'),
                        headers=token, verify=False)

def getAllCredentials(token, udserver):
    """
    Retrieves all credentials via a GET call to the UCMDB REST API.

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
        This can be converted to a list of dictionaries, each representing one
        domain. For example:
        [
            {
                "domainName": "DefaultDomain",
                "description": "",
                "type": "customer",
                "encrypt": false,
                "hashProtocols": {
                    "sshprotocol": [
                        {
                            "hashParameters": {
                                "sshprotocol_sudo_su_policy": "privileged_execution",
                                "protocol_pe_su_username": null,
                                "protocol_username": "root",
                                "sshprotocol_su_username": null,
                                "sshprotocol_prompts": null,
                                "protocol_timeout": "25000",
                                "sshprotocol_sudo_paths": null,
                                "protocol_netaddress": null,
                                "protocol_pe_mode": "su",
                                "protocol_pce_command_list": null,
                                "sshprotocol_shell_env_sep_char": ";",
                                "protocol_in_use": "true",
                                "protocol_pce_policy": "privileged_execution",
                                "external_vault_type": null,
                                "protocol_index": "1",
                                "sshprotocol_hello_timeout": "10000",
                                "external_password_static_key": null,
                                "protocol_port": "22",
                                "user_label": "UCMDB root",
                                "password_vault_type": null,
                                "sshprotocol_authmode": "password",
                                "sshprotocol_sudo_commands": null,
                                "sshprotocol_version": "SSH2/SSH1",
                                "cm_credential_id": "4_1_CMS",
                                "password_vault_reference_id": null,
                                "sshprotocol_keypath": null,
                                "protocol_type": "sshprotocol"
                            },
                            "protocolIndex": 1,
                            "netAddress": null
                        }
                    ]
                }
            }
        ]

    """
    return requests.get(
        _url(udserver, '/dataflowmanagement/credentials'),
        headers=token, verify=False
    )

def getAllProtocols(token, udserver):
    """
    This method will get a dictionary which lists all possible
    protocols via a GET method to the UCMDB server.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution (IP
        or hostname).

    Returns
    -------
    requests.Response
        Can be converted to a dictionary of all possible protocols. For example:
        {
            "AMQP Protocol": "amqpprotocol",
            "AS400 Protocol": "as400protocol",
            "Asset Manager Protocol": "amadapterprotocol",
            "AWS Protocol": "awsprotocol",
            "Azure Protocol": "azureprotocol",
            "CA CMDB Protocol": "cacmdbprotocol",
            "CIM Protocol": "cimprotocol",
            "Generic DB Protocol (NoSQL)": "nosqlprotocol",
            "Generic DB Protocol (SQL)": "sqlprotocol",
            "Generic Protocol": "genericprotocol",
            "Google Cloud Protocol": "google_cloudprotocol",
            "HTTP Protocol": "httpprotocol",
            "JBOSS Protocol": "jbossprotocol",
            "LDAP Protocol": "ldapprotocol",
            "NetApp Protocol": "netappprotocol",
            "Network Automation Java Protocol":
                "networkautomationprotocol",
            "NTCMD Protocol": "ntadminprotocol",
            "Oracle Cloud Protocol": "oracle_cloudprotocol",
            "PowerApps Protocol": "powerappsprotocol",
            "PowerCmd Protocol": "powercmdprotocol",
            "Powershell Protocol (deprecated)":
                "powershellprotocol",
            "Remedy Protocol": "remedyprotocol",
            "Salesforce Rest Protocol": "salesforceprotocol",
            "SAP JMX Protocol": "sapjmxprotocol",
            "SAP Protocol": "sapprotocol",
            "ServiceNow Protocol": "snowprotocol",
            "Siebel Gateway Protocol": "siebelgtwyprotocol",
            "SNMP Protocol": "snmpprotocol",
            "SSH Protocol": "sshprotocol",
            "Telnet Protocol": "telnetprotocol",
            "TIBCO Protocol": "tibcoprotocol",
            "TLS Protocol": "tlsprotocol",
            "UCMDB Protocol": "ucmdbadapterprotocol",
            "UCS Protocol": "ucsprotocol",
            "Universal Discovery Protocol": "udaprotocol",
            "vCloud Protocol": "vcloudprotocol",
            "VMware VIM Protocol": "vmwareprotocol",
            "WebLogic Protocol": "weblogicprotocol",
            "WebSphere Protocol": "websphereprotocol",
            "WMI Protocol": "wmiprotocol"
        }

    """
    return requests.get(
        _url(udserver, '/dataflowmanagement/protocols'),
        headers=token, verify=False
    )

def getCredentialProfiles(token, udserver):
    """
    This method will get a dictionary which lists all current
    protocols instantiated via a GET method to the UCMDB server.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution (IP
        or hostname).

    Returns
    -------
    requests.Response
        Can be converted to a dictionary of all possible protocols. For example:
        {
            "items": [
                {
                    "name": "All Credentials",
                    "id": "All Credentials",
                    "type": "CMS",
                    "oob": true,
                    "credentials": [
                        {
                            "domain": "DefaultDomain",
                            "protocols": {
                                "sshprotocol": [
                                    "4_1_CMS",
                                    "5_1_CMS"
                                ],
                                "ntadminprotocol": [
                                    "2_1_CMS",
                                    "3_1_CMS",
                                    "7_1_CMS",
                                    "8_1_CMS",
                                    "9_1_CMS",
                                    "10_1_CMS"
                                ],
                                "httpprotocol": [
                                    "6_1_CMS"
                                ]
                            }
                        }
                    ]
                }
            ]
        }
    """
    return requests.get(
        _url(udserver, '/discovery/credentialprofiles'),
        headers=token, verify=False
    )

def getProbeInfo(token, udserver):
    """
    This method calls a UCMDB REST API via GET and returns the status
    of data flow probes.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution (IP
        or hostname).

    Returns
    -------
    requests.Response
        Returns a dictionary with a single attribute, 'items' which
        contains a list of the data flow probe information. For example:
        {
            "items": [
                {
                    "probeName": "FTC06UCM43",
                    "description": "",
                    "probeVersion": "24.2.0.232",
                    "probeInternalVersion": "11.8.0.232",
                    "probeStatus": "CONNECTED",
                    "probeIp": "16.71.201.63",
                    "probeOS": "WINDOWS",
                    "domainName": "DefaultDomain",
                    "clusterName": "",
                    "rangeCount": 1,
                    "ipCount": 241,
                    "versionCompatibility": "MATCHED",
                    "upgradeStatus": "NO_ACTION",
                    "lastAccessTime": 1718367907838,
                    "tokenCompatible": true
                }
            ]
        }

    """
    return requests.get(
        _url(udserver, '/dataflowmanagement/probes'),
        headers=token, verify=False
    )

def getProbeRanges(token, probeName, udserver):
    """
    This method retrieves the range information of a specified probe
    via a GET request to the UCMDB REST API.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    probeName : str
        Name of the probe in UCMDB.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution (IP
        or hostname).

    Returns
    -------
    requests.Response
        Dictionary of the probe and a list of all ranges in the probe.
        For example:
        {
            "probeName": "FTC06UCM43",
            "description": "",
            "probeVersion": "24.2.0.232",
            "probeInternalVersion": "11.8.0.232",
            "probeStatus": "CONNECTED",
            "probeIp": "16.71.201.63",
            "probeOS": "WINDOWS",
            "domainName": "DefaultDomain",
            "clusterName": "",
            "rangeCount": 1,
            "ipCount": 241,
            "ranges": [
                [
                    {
                        "probe": null,
                        "range": "16.71.201.15-16.71.201.255",
                        "description": "",
                        "definitionType": 0,
                        "rangeType": 0,
                        "ipVersion": 0,
                        "excluded": false
                    }
                ]
            ],
            "versionCompatibility": "MATCHED",
            "upgradeStatus": "NO_ACTION",
            "lastAccessTime": 1718368208205,
            "tokenCompatible": false
        }
    """
    probeURL = '/dataflowmanagement/probes/' + probeName
    return requests.get(
        _url(udserver, probeURL),
        headers=token, verify=False
    )

def getProtocol(token, udserver, protocol_id):
    """
    Retrieves the attributes and types of a specified protocol via a
    GET request to the UCMDB REST API.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution (IP
        or hostname).
    protocol_id : str
        The type of protocol. Must be in this list:
            amqpprotocol, as400protocol, amadapterprotocol, awsprotocol,
            azureprotocol, cacmdbprotocol, cimprotocol, nosqlprotocol,
            sqlprotocol, genericprotocol, google_cloudprotocol,
            httpprotocol, jbossprotocol, ldapprotocol, netappprotocol,
            networkautomationprotocol, ntadminprotocol,
            oracle_cloudprotocol, powerappsprotocol, powercmdprotocol,
            powershellprotocol, remedyprotocol, salesforceprotocol,
            sapjmxprotocol, sapprotocol, snowprotocol, siebelgtwyprotocol,
            snmpprotocol, sshprotocol, telnetprotocol, tibcoprotocol,
            tlsprotocol, ucmdbadapterprotocol, ucsprotocol, udaprotocol,
            vcloudprotocol, vmwareprotocol, weblogicprotocol,
            websphereprotocol, wmiprotocol.

    Returns
    -------
    requests.Response
        Returns a dictionary with all the attributes and types of a given
        protocol. For example:
        {
            "protocolAttributeList": {
                "generalProperties": [
                    {
                        "attributeName": "user_label",
                        "displayName": "User Label",
                        "type": "string",
                        "order": 0
                    },
                    {
                        "attributeName": "protocol_timeout",
                        "displayName": "Connection Timeout [msec]",
                        "type": "integer",
                        "defaultValue": "20000",
                        "order": 0
                    },
                    {
                        "attributeName": "external_vault_type",
                        "displayName": "External Vault Type",
                        "type": "string",
                        "order": 0
                    },
                    {
                        "attributeName": "protocol_username",
                        "displayName": "User Name",
                        "defaultValue": "",
                        "type": "string",
                        "order": 0
                    },
                    {
                        "attributeName": "protocol_password",
                        "displayName": "User Password",
                        "type": "bytes",
                        "order": 0,
                        "Qualifiers": [
                            "ENCRYPTED_ATTRIBUTE"
                        ]
                    },
                    {
                        "attributeName": "external_password_static_key",
                        "displayName": "Reference",
                        "type": "string",
                        "order": 0
                    },
                    {
                        "attributeName": "ntadminprotocol_ntdomain",
                        "displayName": "Windows Domain",
                        "type": "string",
                        "order": 0
                    },
                    {
                        "attributeName": "ntadminprotocol_service_startup",
                        "displayName": "Run remote commands impersonated",
                        "type": "string",
                        "defaultValue": "LocalService",
                        "valueList": [
                            "LocalService",
                            "User"
                        ],
                        "order": 0
                    },
                    {
                        "attributeName": "ntadminprotocol_remote_share_alias",
                        "displayName": "Remote Share Path",
                        "type": "string",
                        "order": 0
                    },
                    {
                        "attributeName": "ntadminprotocol_remote_share_path",
                        "displayName": "Share Local Path",
                        "type": "string",
                        "order": 0
                    }
                ]
            },
            "protocolAttributeDisplayList": {
                "protocol_username": [
                    {
                        "attributeName": "external_vault_type",
                        "value": "Internal"
                    }
                ],
                "protocol_password": [
                    {
                        "attributeName": "external_vault_type",
                        "value": "Internal"
                    }
                ],
                "external_password_static_key": [
                    {
                        "attributeName": "external_vault_type",
                        "value": "CyberArk"
                    },
                    {
                        "attributeName": "external_vault_type",
                        "value": "SAP"
                    }
                ]
            },
            "dynamicAttributeList": {
                "external_vault_type": {
                    "attributeName": "external_vault_type",
                    "valueList": [
                        "Internal"
                    ],
                    "order": 0
                }
            },
            "protocolAttributeValidteList": {
                "external_password_static_key": [
                    "externalVaultReferenceFormat",
                    "presence"
                ]
            },
            "isNewProtocolParameter": true,
            "protocolName": "ntadminprotocol"
        }
    """
    return requests.get(
        _url(udserver, '/dataflowmanagement/protocols/' + protocol_id),
        headers=token, verify=False
    )

def probeStatus(token, udserver):
    """
    This method queries the UCMDB server and gets information about the
    status of the probe including CPU, RAM, Disk, etc.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution (IP
        or hostname).

    Returns
    -------
    requests.Response
        Returns a dictionary containing the probe and information about the
        probe. For example:
        {
            "FTC06UCM43": {
                "fips": false,
                "zoneBased": true,
                "domainName": "DefaultDomain",
                "probeName": "FTC06UCM43",
                "probeStatus": "Well",
                "ip": "16.71.201.63",
                "cpuUsage": 58.46154,
                "ramUsage": 96.64884,
                "totalRam": 12884,
                "usedRam": 12452,
                "harddiskUsage": 47.97787,
                "totalHarddisk": 128321,
                "usedHarddisk": 61565,
                "discoveredCI": 956555,
                "unSentCI": 0,
                "runningJob": 0,
                "totalJob": 14,
                "finishedJobNumber": 14,
                "scheduledJobNumber": 14,
                "blockedJobNumber": 0,
                "removedJobNumber": 0,
                "unsendJobNumber": 0,
                "activeWorker": 0,
                "totalWorker": 80,
                "jobSimpleRuntimeInfoWrapperMap": {},
                "probeDiscoveryStatsMap": null,
                "externalVersion": "24.2.0.232",
                "tenantName": "",
                "totalHeapSize": 2147,
                "currentHeapUsage": 579,
                "heapUsage": 26.992249,
                "isFIPS": false,
                "certValidationLevel": 2,
                "customerID": "1",
                "serverName": "FTC06UCM43",
                "lastUpdateTime": 1718372135000,
                "isZoneBased": true
            }
        }

    """
    return requests.get(_url(udserver, '/uiserver/probeService/dashboard/summary'
                             ), headers=token, verify=False)

def probeStatusDetails(token, udserver, domain, probe):
    """
    This method uses a GET call to the REST API of UCMDB to get the
    detailed status of a probe.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution (IP
        or hostname).
    domain : str
        Domain of the probe to get. The default value is 'DefaultDomain'.
    probe : str
        The name of the probe.

    Returns
    -------
    requests.Response
        Contains detailed information about the probe and jobs running
        on it. For example:
        {
            "fips": false,
            "zoneBased": true,
            "domainName": "DefaultDomain",
            "probeName": "FTC06UCM43",
            "probeStatus": "Well",
            "ip": "16.71.201.63",
            "cpuUsage": 60.76923,
            "ramUsage": 96.74656,
            "totalRam": 12884,
            "usedRam": 12465,
            "harddiskUsage": 47.97838,
            "totalHarddisk": 128321,
            "usedHarddisk": 61566,
            "discoveredCI": 956555,
            "unSentCI": 0,
            "runningJob": 0,
            "totalJob": 14,
            "finishedJobNumber": 14,
            "scheduledJobNumber": 14,
            "blockedJobNumber": 0,
            "removedJobNumber": 0,
            "unsendJobNumber": 0,
            "activeWorker": 0,
            "totalWorker": 80,
            "jobSimpleRuntimeInfoWrapperMap": {
                "ZONE_zone 1_JOB_Range IPs by ICMP": {
                    "jobName": "ZONE_zone 1_JOB_Range IPs by ICMP",
                    "zoneId": "zone 1",
                    "jobId": "Range IPs by ICMP",
                    "progress": 0,
                    "threadNumber": 0,
                    "totalTrigger": 1,
                    "succeededTriggerCI": 1,
                    "previousInvocationTime": 1718301527000,
                    "nextInvocationTime": 1718387927000,
                    "objectsWaitingInQueue": 0,
                    "lastDuration": 14,
                    "averageDuration": 14.032,
                    "recurence": 34,
                    "status": "Scheduled"
                }
            },
            "probeDiscoveryStatsMap": {
                "file_system": {
                    "createdcount": 0,
                    "updatedcount": 0,
                    "removedcount": 122,
                    "ignoredcount": 0,
                    "invalidcount": 0,
                    "totalcount": 122,
                    "failed": 0,
                    "unidentified": 0
                },
                "installed_software": {
                    "createdcount": 0,
                    "updatedcount": 0,
                    "removedcount": 3,
                    "ignoredcount": 0,
                    "invalidcount": 0,
                    "totalcount": 3,
                    "failed": 0,
                    "unidentified": 0
                },
                "usage": {
                    "createdcount": 0,
                    "updatedcount": 0,
                    "removedcount": 4,
                    "ignoredcount": 0,
                    "invalidcount": 0,
                    "totalcount": 4,
                    "failed": 0,
                    "unidentified": 0
                }
            },
            "externalVersion": "24.2.0.232",
            "tenantName": "",
            "totalHeapSize": 2147,
            "currentHeapUsage": 579,
            "heapUsage": 26.992249,
            "isFIPS": false,
            "certValidationLevel": 2,
            "customerID": "1",
            "serverName": "FTC06UCM43",
            "lastUpdateTime": 1718372666000,
            "isZoneBased": true
        }

    """
    return requests.get(
        _url(udserver, 
             f'/uiserver/probeService/dashboard/domain/{domain}/probe/{probe}/runtime'
        ), 
        headers=token, 
        verify=False
    )

def queryIPs(token, udserver, ip_addr):
    """
    This method uses a GET call to the UCMDB REST API to determine
    which, if any, probe has a given IP Address in its ranges.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass,
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution
        (IP or hostname).
    ip_addr : str
        The IP Address to find (e.g. 10.1.1.1).

    Returns
    -------
    requests.Response
        If found, returns the probe in a dictionary with a single
        entry called items, which is a list of dictionaries the IP
        address is in. Otherwise returns a dictionary with items
        and the list is empty. For example:
        {
            "items": [
                {
                    "probeName": "FTC06UCM43",
                    "description": "",
                    "probeVersion": "24.2.0.232",
                    "probeInternalVersion": "11.8.0.232",
                    "probeStatus": "CONNECTED",
                    "probeIp": "16.71.201.63",
                    "probeOS": "WINDOWS",
                    "domainName": "DefaultDomain",
                    "clusterName": "",
                    "rangeCount": 1,
                    "ipCount": 241,
                    "versionCompatibility": "MATCHED",
                    "upgradeStatus": "NO_ACTION",
                    "lastAccessTime": 1718373382106,
                    "tokenCompatible": true
                }
            ]
        }

        or, if not found:
        {
            "items": []
        }
    """
    return requests.get(
        _url(udserver, 
             f'/dataflowmanagement/probes?queriedIpAddress={ip_addr}'
        ), 
        headers=token, 
        verify=False
    )
