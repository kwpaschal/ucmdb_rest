# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:16:59 2024

@author: kpaschal

This module contains methods to work with CMS UI jobs inside the CMS UI
discovery framework.
"""

import requests
from urllib.parse import quote

from .utils import _url

def createJobGroup(token, udserver, job_group):
    """
    Creates a job group with the job_group specified.

    This function makes a POST request to the UCMDB server to 
    create a job group.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution 
        (IP or hostname).
    job_group : dict
        A dictionary containing the job group to be created. Example:
            {
              "name": "string",
              "description": "string",
              "jobs": [
                {
                  "jobName": "string",
                  "jobDisplayName": "string",
                  "adapterName": "string",
                  "inputCI": "string",
                  "jobType": "string",
                  "protocols": [
                    "string"
                  ],
                  "jobParameters": {
                    "additionalProp1": "string",
                    "additionalProp2": "string",
                    "additionalProp3": "string"
                  },
                  "triggerQueries": [
                    "string"
                  ],
                  "jobInvokeOnNewTrigger": true
                }
              ]
            }

    Returns
    -------
    requests.Response
        A dictionary containing the job group.

    Example
    -------
    Example Output:
    {
      "name": "Hardware_Only-AgentBased",
      "id": "Hardware_Only-AgentBased",
      "type": "CMS",
      "oob": false,
      "description": "Hardware/Server config inventory using UDAgent",
      "discoveryType": null,
      "jobs": [
        {
          "jobName": "Call Home Processing",
          "jobDisplayName": "Call Home Processing",
          "adapterName": "CallHomeProcessing",
          "inputCI": "callhome_event",
          "jobType": "DynamicService",
          "protocols": [],
          "jobParameters": {},
          "triggerQueries": [],
          "jobInvokeOnNewTrigger": true
        }
      ]
    }
    """
    return requests.post(
        _url(udserver, '/discovery/discoveryprofiles'),
        headers=token, 
        json=job_group, 
        verify=False
    )

def deleteSpecificJobGroup(token, udserver, job_group):
    """
    Deletes a job group.

    This function makes a DELETE request to the UCMDB server to 
    delete a job group.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution 
        (IP or hostname).
    job_group : str
        The name of the job group to delete.

    Returns
    -------
    requests.Response
        Status code:
        - 200 : Success
        - 400 : Bad Request
        - 401 : Unauthorized
        - 404 : Resource Not Found
        - 500 : Internal Server Error

    """
    return requests.delete(
        _url(udserver, '/discovery/discoveryprofiles/' + job_group),
        headers=token, 
        verify=False
    )

def getIPRange(token, udserver):
    """
    Retrieves IP range profiles from the UCMDB server.

    This method makes a GET request to the UCMDB server to retrieve IP 
    range profiles.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.

    Returns
    -------
    requests.Response
        Response object containing the IP range profiles.

    Summary of Output
    -----------------
    The output represents a list of items, each describing a location or 
    group of IP range profiles. Each item contains the following 
    information:

    - Name: The name of the location or group.
    - ID: Unique identifier for the location or group.
    - Type: Type of the location or group.
    - OOB: Indicates if the location or group is Out Of Band (OOB).
    - Ranges: List of IP range profiles associated with the location or 
      group. Each range contains information about the domain name, 
      cluster name, probe name, and IP ranges.
    - RangeCount: Total number of IP range profiles within the location 
      or group.
    - IPAddressCount: Total number of IP addresses covered by the IP 
      range profiles within the location or group.

    Example
    -------
    >>> token = {'auth_token': 'example_token'}
    >>> udserver = 'example_ucmdb_server'
    >>> response = getIPRange(token, udserver)
    >>> ip_ranges = response.json()['items']
    >>> for item in ip_ranges:
    >>>     print(f"Probe Name: {item['name']}, Total IPs: "
    >>>           f"{item['ipAddressCount']}")
    """
    return requests.get(
        _url(udserver, '/discovery/iprangeprofiles'),
        headers=token, 
        verify=False
    )

def getIPRangeForIP(token, udserver, ipaddr):
    """
    Retrieves IP range profiles associated with a specific IP address 
    from the UCMDB server.

    This method makes a GET request to the UCMDB server to retrieve IP 
    range profiles associated with a specific IP address.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    ipaddr : str
        IP address for which to retrieve IP range profiles.

    Returns
    -------
    requests.Response
        Response object containing the IP range profiles associated 
        with the specified IP address.

    Example
    -------
    >>> token = {'auth_token': 'example_token'}
    >>> udserver = 'example_ucmdb_server'
    >>> ipaddr = '192.168.1.100'
    >>> response = getIPRangeForIP(token, udserver, ipaddr)
    >>> ip_ranges = response.json()['items']
    >>> for item in ip_ranges:
    >>>     print(f"Probe Name: {item['name']}, Total IPs: "
    >>>           f"{item['ipAddressCount']}")
    """
    return requests.get(
        _url(udserver, '/discovery/iprangeprofiles?ipaddress=' + str(ipaddr)),
        headers=token, 
        verify=False
    )

def getJobGroup(token, udserver, fields =''):
    """
    Retrieves a structure of jobs groups discovery.

    This function makes a GET request to the UCMDB server to 
    retrieve the job group information.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution 
        (IP or hostname).
    fields : list of str, optional
        A comma separated list of strings E.g. name,id.

    Returns
    -------
    requests.Response
        A dictionary with a list of dictionaries. Each 
        subdictionary in the list contains a response representing 
        a job group for discovery. The structure includes:
        - name: The name of the discovery job group.
        - id: The id of the job group.
        - type: CMS.
        - oob: false.
        - description: The description of the discovery job group in 
          the UI.
        - discoveryType: usually null.
        - jobs: A list of dictionaries representing the job.
            - jobName: The name of the discovery job included.
            - jobDisplayName: The display name of the discovery job.
            - adapterName: The name of the adapter the job is based on.
            - inputCi: The input CI for the job.
            - protocols: A list of protocols used by this job.
            - jobParameters: A dictionary of parameter:value.
            - triggerQueries: A list of the trigger queries.
            - jobInvokeOnNewTrigger: true/false. Does the job 
              execute on new triggers immediately or wait until the 
              next scheduled invocation.

    Example
    -------
    Example Output:
    {
      "items": [
        {
          "name": "HRA",
          "id": "HRA",
          "type": "CMS",
          "oob": false,
          "description": null,
          "discoveryType": null,
          "jobs": [
            {
              "jobName": "Host Connection by Shell",
              "jobDisplayName": "Host Connection by Shell",
              "adapterName": "Host_Connection_By_Shell",
              "inputCI": "ip_address",
              "jobType": "DynamicService",
              "protocols": [
                "ntadminprotocol",
                "sshprotocol",
                "telnetprotocol",
                "udaprotocol",
                "powercmdprotocol"
              ],
              "jobParameters": {},
              "triggerQueries": [],
              "jobInvokeOnNewTrigger": true
            },
            {
              "jobName": "Range IPs by ICMP",
              "jobDisplayName": "Range IPs by ICMP",
              "adapterName": "ICMP_NET_Dis_IpRange",
              "inputCI": "discoveryprobegateway",
              "jobType": "DynamicService",
              "protocols": [],
              "jobParameters": {},
              "triggerQueries": [],
              "jobInvokeOnNewTrigger": true
            }
          ]
        }
      ]
    }
    """
    if fields == '':
        myUrl = _url(udserver, '/discovery/discoveryprofiles')
    else:
        fields = quote(fields)
        myUrl = _url(udserver, '/discovery/discoveryprofiles?fields='+fields)
    return requests.get(
        myUrl, 
        headers=token, 
        verify=False
    )

def getJobMetaData(token, udserver):
    """
    Retrieves a structure of jobs for discovery.

    This function makes a GET request to the UCMDB server to 
    retrieve the module tree information.

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
        A dictionary with a list of dictionaries. Each 
        subdictionary in the list contains response representing 
        a job for discovery. The structure includes:
        - name: The name of the discovery job.
        - id: The id of the job.
        - type: usually null.
        - oob: usually null.
        - jobDisplayName: The name of the discovery job in the UI.
        - adapterName: The name of the adapter for this discovery 
          job.
        - tags: A list of tags for the job.
        - dependOnJobs: A list of jobs this one is dependent upon.
        - moduleName: The name of the containing module.
        - jobType: DynamicService or Workflow.
        - inputCi: The input CI for the job.
        - outputCis: The CIs created by this job.
        - flat: boolean flag (all ootb are set to false).
        - protocols: A list of protocols used by this job.
        - discoveryType: BASIC, ADVANCED or sometimes null for what 
          kind of license is used consumed as a result of this job.
        - inputCiDisplayName: Display name of the input CI.
        - outputCiDisplayName: A list containing the display name of 
          the output CIs.
        - protocolsDisplayName: A list containing the protocols 
          display labels.

    Example
    -------
    Example Output:
    {
      "items": [
        {
          "name": "A10 vThunder by SNMP",
          "id": "A10 vThunder by SNMP",
          "type": null,
          "oob": null,
          "jobDisplayName": "A10 vThunder by SNMP",
          "adapterName": "A10_vThunder_by_SNMP",
          "tags": [
            "Load Balancer"
          ],
          "dependOnJobs": [
            "Host Connection by SNMP"
          ],
          "moduleName": "A10 vThunder",
          "jobType": "DynamicService",
          "inputCi": "snmp",
          "outputCis": [
            "a10_vthunder",
            "composition",
            "configuration_document",
            "containment",
            "ip_address",
            "ip_service_endpoint",
            "lb",
            "loadbalancecluster",
            "membership",
            "node",
            "ownership"
          ],
          "flat": false,
          "protocols": [
            "snmpprotocol"
          ],
          "discoveryType": "ADVANCED",
          "inputCiDisplayName": "SNMP",
          "outputCiDisplayName": [
            "A10 vThunder",
            "Composition",
            "ConfigurationDocument",
            "Containment",
            "IpAddress",
            "IpServiceEndpoint",
            "Load Balancer",
            "Load Balancing Cluster",
            "Membership",
            "Node",
            "Ownership"
          ],
          "protocolsDisplayName": [
            "SNMP Protocol"
          ]
        }
      ]
    }
    """
    return requests.get(
        _url(udserver, '/discovery/discoverymetadata/jobmetadata'),
        headers=token, 
        verify=False
    )

def getModuleTree(token, udserver):
    """
    Retrieves a hierarchical structure of modules and jobs for discovery.

    This function makes a GET request to the UCMDB server to retrieve
    the module tree information.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 'createHeaders'
        with arguments of ucmdb_user, ucmdb_pass, and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution (IP or 
        hostname).

    Returns
    -------
    requests.Response
        A JSON response representing a hierarchical structure of modules 
        and jobs for discovery. The structure includes:
        - name: The name of the use case.
        - path: The path of the current folder.
        - children: A list of dictionaries containing recursive directories 
                    and modules.
        - jobs: At the bottom level, a list of jobs in a given path.

    Example
    -------
    Example Output:
    {
      "name": "Discovery Modules",
      "path": "full path",
      "children": [
        {
          "name": "Middleware",
          "path": "Middleware\\\\Web Services\\\\UDDI Registry",
          "children": [
            {
              "name": "Web Services",
              "path": "Middleware\\\\Web Services\\\\UDDI Registry",
              "children": [
                {
                  "name": "UDDI Registry",
                  "path": "Middleware\\\\Web Services\\\\UDDI Registry",
                  "children": [],
                  "jobs": [
                    "Webservices by UDDI Registry",
                    "Webservice Connections by UDDI Registry",
                    "WebServices by URL"
                  ]
                }
              ],
              "jobs": null
            }
          ]
        }
      ]
    }
    """
    return requests.get(
        _url(udserver, '/discovery/discoverymetadata/moduletree'),
        headers=token, 
        verify=False
    )

def getQuestions(token, udserver, job_name):
    """
    Retrieves questions for a specific discovery job.

    This function makes a GET request to the UCMDB server to 
    retrieve the questions for a specific discovery job.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution 
        (IP or hostname).
    job_name : str
        The job name, for example 'Host Connection by Shell'.

    Returns
    -------
    requests.Response
        A dictionary object containing the questions for the 
        parameters. Example:
        {
          "questions": [
            {
              "questionTextAlt": 
                  "Specify the Universal Discovery Protocol connection order",
              "questionTextL10ID": 
                  "QUESTION_HOST_CONNECTION_BY_SHELL_0",
              "helpID": "",
              "questionType": "DropDownList",
              "tag": "",
              "groupId": "",
              "groupType": "",
              "dependency": "",
              "dependencyCondition": "",
              "choices": [
                {
                  "choiceText": "first",
                  "choiceTextL10Key": 
                      "QUESTION_HOST_CONNECTION_BY_SHELL_0_CHOICE_0",
                  "defaultState": "Unchecked",
                  "behavior": "Parameter Change",
                  "mappingToJobs": [],
                  "mappingToParams": {
                    "Host Connection by Shell": {
                      "udaConnectionOrder": "first"
                    }
                  }
                },
                {
                  "choiceText": "last",
                  "choiceTextL10Key": 
                      "QUESTION_HOST_CONNECTION_BY_SHELL_0_CHOICE_1",
                  "defaultState": "Checked",
                  "behavior": "Parameter Change",
                  "mappingToJobs": [],
                  "mappingToParams": {
                    "Host Connection by Shell": {
                      "udaConnectionOrder": "last"
                    }
                  }
                },
                {
                  "choiceText": "none",
                  "choiceTextL10Key": 
                      "QUESTION_HOST_CONNECTION_BY_SHELL_0_CHOICE_2",
                  "defaultState": "Unchecked",
                  "behavior": "Parameter Change",
                  "mappingToJobs": [],
                  "mappingToParams": {
                    "Host Connection by Shell": {
                      "udaConnectionOrder": "none"
                    }
                  }
                }
              ]
            }
          ],
          "jobQuestions": [
            {
              "name": "Host Connection by Shell",
              "id": null,
              "type": null,
              "oob": true,
              "questions": [
                {
                  "questionTextAlt": 
                      "Specify the Universal Discovery Protocol connection order",
                  "questionTextL10ID": 
                      "QUESTION_HOST_CONNECTION_BY_SHELL_0",
                  "helpID": "",
                  "questionType": "DropDownList",
                  "tag": "",
                  "groupId": "",
                  "groupType": "",
                  "dependency": "",
                  "dependencyCondition": "",
                  "choices": [
                    {
                      "choiceText": "first",
                      "choiceTextL10Key": 
                          "QUESTION_HOST_CONNECTION_BY_SHELL_0_CHOICE_0",
                      "defaultState": "Unchecked",
                      "behavior": "Parameter Change",
                      "mappingToJobs": [],
                      "mappingToParams": {
                        "Host Connection by Shell": {
                          "udaConnectionOrder": "first"
                        }
                      }
                    },
                    {
                      "choiceText": "last",
                      "choiceTextL10Key": 
                          "QUESTION_HOST_CONNECTION_BY_SHELL_0_CHOICE_1",
                      "defaultState": "Checked",
                      "behavior": "Parameter Change",
                      "mappingToJobs": [],
                      "mappingToParams": {
                        "Host Connection by Shell": {
                          "udaConnectionOrder": "last"
                        }
                      }
                    },
                    {
                      "choiceText": "none",
                      "choiceTextL10Key": 
                          "QUESTION_HOST_CONNECTION_BY_SHELL_0_CHOICE_2",
                      "defaultState": "Unchecked",
                      "behavior": "Parameter Change",
                      "mappingToJobs": [],
                      "mappingToParams": {
                        "Host Connection by Shell": {
                          "udaConnectionOrder": "none"
                        }
                      }
                    }
                  ]
                }
              ],
              "tags": null
            }
          ]
        }

    """
    job_name = quote(job_name)
    return requests.get(
        _url(udserver, 
             '/discovery/discoverymeta/tags/questions?jobNames=' + job_name),
        headers=token, 
        verify=False
    )

def getSchedules(token, udserver):
    """
    Retrieves a list of all schedules.

    This function makes a GET request to the UCMDB server to 
    retrieve a list of schedules.

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
        A dictionary object containing the schedules. Example:
        {
          "items": [
            {
              "name": "MWF",
              "id": "MWF",
              "type": "CMS",
              "oob": false,
              "scheduleDetail": {
                "invocationTime": null,
                "intervalUnit": null,
                "interval": null,
                "invocationHours": [
                  "17:00"
                ],
                "daysOfWeek": [
                  2,
                  4,
                  6
                ],
                "monthsOfYear": null,
                "daysOfMonth": null,
                "cronExpr": null
              },
              "runDuringTimeRange": {
                "type": "always",
                "timeRange": null,
                "alwaysRunBetween": null
              },
              "startTime": null,
              "endTime": null,
              "timeZone": null,
              "scheduleType": "scheduler_cron_Schedule",
              "cronExpression": 
                  "0 0 17 ? * 2 ;0 0 17 ? * 4 ;0 0 17 ? * 6",
              "offset": null,
              "generateFrom": "WEEKLY",
              "templateType": null,
              "templateSource": null
            }
          ]
        }
    """
    return requests.get(
        _url(udserver, '/discovery/scheduleprofiles'), 
        headers=token, 
        verify=False
    )

def getSpecificJobGroup(token, udserver, job_group):
    """
    Retrieves a job group.

    This function makes a GET request to the UCMDB server to 
    retrieve a job group.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB Server hostname that is valid from DNS resolution 
        (IP or hostname).
    job_group : str
        The name of the job group to retrieve.

    Returns
    -------
    requests.Response
        A dictionary object containing the job group. Example:
        {
          "name": "HRA",
          "id": "HRA",
          "type": "CMS",
          "oob": false,
          "description": null,
          "discoveryType": null,
          "jobs": [
            {
              "jobName": "Host Connection by Shell",
              "jobDisplayName": "Host Connection by Shell",
              "adapterName": "Host_Connection_By_Shell",
              "inputCI": "ip_address",
              "jobType": "DynamicService",
              "protocols": [
                "ntadminprotocol",
                "sshprotocol",
                "telnetprotocol",
                "udaprotocol",
                "powercmdprotocol"
              ],
              "jobParameters": {},
              "triggerQueries": [],
              "jobInvokeOnNewTrigger": true
            },
            {
              "jobName": "Range IPs by ICMP",
              "jobDisplayName": "Range IPs by ICMP",
              "adapterName": "ICMP_NET_Dis_IpRange",
              "inputCI": "discoveryprobegateway",
              "jobType": "DynamicService",
              "protocols": [],
              "jobParameters": {},
              "triggerQueries": [],
              "jobInvokeOnNewTrigger": true
            }
          ]
        }

    """
    return requests.get(
        _url(udserver, '/discovery/discoveryprofiles/' + str(job_group)),
        headers=token, 
        verify=False
    )

def getUseCase(token, udserver):
    """
    Retrieves a hierarchical structure of use cases for discovery.
    
    This method makes a GET request to the UCMDB server to retrieve
    the information.

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
    direquests.Responsect
        A JSON representing a hierarchical structure of use cases 
        for discovery. Each use case contains:
        - name: The name of the use case.
        - checked: A boolean value indicating if it's checked.
        - display: A boolean value indicating if it's displayed.
        - children: A list of dictionaries representing child use 
          cases. Each child contains:
            - name: The name of the child use case.
            - checked: A boolean value indicating if it's checked.
            - display: A boolean value indicating if it's displayed.
            - children: A list of dictionaries representing nested 
              children. (This structure forms a hierarchical tree 
              of use cases.)

    Example
    -------
    Example Output:
    [
        {
            "name": "Discovery",
            "checked": false,
            "display": false,
            "children": [
                {
                    "name": "Network and Hosts",
                    "checked": false,
                    "display": true,
                    "children": [
                        {
                            "name": "Network and Host Information",
                            "checked": true,
                            "display": null,
                            "children": null
                        },
                        ...
                    ]
                },
                ...
            ]
        },
        ...
    ]
    """
    return requests.get(
        _url(udserver, '/discovery/discoverymetadata/usecases'),
        headers=token, 
        verify=False
    )