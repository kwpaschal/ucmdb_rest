# -*- coding: utf-8 -*-
"""
UCMDB Discovery Service

This module provides an interface for managing the CMS UI Discovery framework. 
It allows for the programmatic management of Discovery Jobs, Job Groups, 
and Discovery Profiles.

Functional Areas:
1. Job Groups: Create, delete, and list groups of discovery jobs.
2. Discovery Profiles: Manage profiles and their associated job groups.
3. Discovery Metadata: Inspect available discovery use cases and jobs.

Exposed Methods:
    createJobGroup, deleteJobGroup, getJobGroups,
    createProfile, deleteProfile, getProfile, getProfiles,
    getDiscoveryUseCases
"""

from urllib.parse import quote


class Discovery:
    def __init__(self, server):
        """
        Initialize the service with a reference to the main level UCMDB server
        """
        self.server = server
        self.profile_path = '/discovery/discoveryprofiles'

    def _get_profile_url(self, job_group=None):
        """Internal helper for profile URLs"""
        if job_group:
            return f"{self.profile_path}/{quote(job_group)}"
        return self.profile_path

    def createJobGroup(self, job_group):
        """
        Creates a new Discovery Job Group.

        Parameters
        ----------
        job_group : dict
            A dictionary defining the job group.
            Example:
            {
              "name": "Inventory_Group",
              "description": "Custom inventory jobs",
              "jobs": [
                {"jobName": "Host Connection by Shell", "isActivated": true},
                {"jobName": "Host Applications by Shell", "isActivated": true}
              ]
            }

        Returns
        -------
        requests.Response
            The response from the UCMDB server.
        """
        return self.server._request("POST",self._get_profile_url(), json=job_group)

    def createProfile(self, profile_name, job_groups):
        """
        Creates a Discovery Profile and assigns job groups to it.

        Parameters
        ----------
        profile_name : str
            The unique name for the new profile.
        job_groups : list of str
            A list of existing job group names to be included in this profile.
            Example: ["Inventory Jobs", "Network Discovery"]

        Returns
        -------
        requests.Response
        """
        payload = {
            "name": profile_name,
            "jobGroups": [{"name": group} for group in job_groups]
        }
        url = self._get_profile_url()
        return self.server._request("POST",url,json=payload)

    def deleteProfile(self, profile_name):
        """
        Deletes a Discovery Profile by name.

        Parameters
        ----------
        profile_name : str
            The name of the profile to delete.

        Returns
        -------
        requests.Response
        """
        url = self._get_profile_url(profile_name)
        return self.server._request("DELETE",url)

    def deleteSpecificJobGroup(self, job_group):
        """
        Deletes a job group.

        This function makes a DELETE request to the UCMDB server to 
        delete a job group.

        Parameters
        ----------
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
        return self.server._request("DELETE",self._get_profile_url(job_group))

    def getIPRange(self):
        """
        Retrieves IP range profiles from the UCMDB server.

        This method makes a GET request to the UCMDB server to retrieve IP 
        range profiles.

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

        """
        url = '/discovery/iprangeprofiles'
        return self.server._request("GET",url)

    def getIPRangeForIP(self, ipaddr):
        """
        Retrieves IP range profiles associated with a specific IP address 
        from the UCMDB server.

        This method makes a GET request to the UCMDB server to retrieve IP 
        range profiles associated with a specific IP address.

        Parameters
        ----------
        ipaddr : str
            IP address for which to retrieve IP range profiles.

        Returns
        -------
        requests.Response
            Response object containing the IP range profiles associated 
            with the specified IP address.

        """
        url = f'/discovery/iprangeprofiles?ipaddress={ipaddr}'
        return self.server._request("GET",url)

    def getJobGroup(self, fields =''):
        """
        Retrieves a structure of jobs groups discovery.

        This function makes a GET request to the UCMDB server to 
        retrieve the job group information.

        Parameters
        ----------
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
        if not fields:
            url = self._get_profile_url()
        else:
            url = f'{self._get_profile_url()}?fields={quote(fields)}'
        return self.server._request("GET",url)

    def getJobMetaData(self):
        """
        Retrieves a structure of jobs for discovery.

        This function makes a GET request to the UCMDB server to 
        retrieve the module tree information.

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
        url = '/discovery/discoverymetadata/jobmetadata'
        return self.server._request("GET",url)

    def getModuleTree(self):
        """
        Retrieves a hierarchical structure of modules and jobs for discovery.

        This function makes a GET request to the UCMDB server to retrieve
        the module tree information.

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
        url = '/discovery/discoverymetadata/moduletree'
        return self.server._request("GET",url)

    def getQuestions(self, job_name):
        """
        Retrieves questions for a specific discovery job.

        This function makes a GET request to the UCMDB server to 
        retrieve the questions for a specific discovery job.

        Parameters
        ----------
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
                    ...
                  ]
                }
              ],
              "jobQuestions": [...]
            }
        """
        job_name = quote(job_name)
        url = f'/discovery/discoverymeta/tags/questions?jobNames={job_name}'
        return self.server._request("GET",url)

    def getSchedules(self):
        """
        Retrieves a list of all schedules.

        This function makes a GET request to the UCMDB server to 
        retrieve a list of schedules.

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
        url = '/discovery/scheduleprofiles'
        return self.server._request("GET",url)

    def getSpecificJobGroup(self, job_group):
        """
        Retrieves a job group.

        This function makes a GET request to the UCMDB server to 
        retrieve a job group.

        Parameters
        ----------
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
        return self.server._request("GET",self._get_profile_url(job_group))

    def getDiscoveryUseCases(self):
        """
        Retrieves the hierarchical tree of Discovery Use Cases.

        This is useful for building a UI or identifying the correct 
        'name' for specific discovery categories.

        Returns
        -------
        requests.Response
            A JSON array of use-case objects containing 'name', 'checked', 
            'display', and 'children' (recursive).
        """
        url = '/discovery/discoverymetadata/usecases'
        return self.server._request("GET",url)