# -*- coding: utf-8 -*-
"""
UCMDB Policies and Compliance Service

This module provides methods to manage UCMDB policies and retrieve compliance 
reports. Policies allow for the automated checking of CIs against specific 
configurations or security standards.

Exposed Methods:
    calculateComplianceView, getComplianceViews, getPolicies, 
    getSpecificComplianceView
"""
from enum import Enum
from urllib.parse import quote


class ComplianceStatus(Enum):
    """Enumeration for valid UCMDB Compliance Status types."""
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON-COMPLIANT"
    NON_APPLICABLE = "NON-APPLICABLE"

class Policies:
    def __init__(self, client):
        """
        Initialize the service with a reference to the main level UCMDB client
        """
        self.client = client

    def calculateComplianceView(self, myDict):
        """
        Calculates compliance based on provided data.

        This method makes a POST request to the UCMDB server to calculate
        compliance based on the provided data.

        Parameters
        ----------
        myDict : dict
            Data to be used for compliance calculation.

        Returns
        -------
        requests.Response
            Response object from the UCMDB server.

        Example
        -------
        >>> my_dict = {'data': 'example_data'}
        >>> response = calculateComplianceView(my_dict)
        >>> print(response.status_code)
        200
        """
        url = f'{self.client.base_url}/policy/calculate?chunkSize=300'
        return self.client.session.post(url, json=myDict)

    def calculateView(self, view):
        """
        Calculates a compliance view based on policies that exist in a
        UCMDB system.

        This method makes a POST request to the UCMDB server to calculate a
        compliance view. The results are a list of dictionaries containing
        the COMPLIANT, NON-COMPLIANT, and NON-APPLICABLE values. The view
        must be from the list created by getComplainceViews.

        Parameters
        ----------
        view : str
            The name of the view to request. The view name will be 
            URL-encoded, so it can contain spaces or special characters.

        Returns
        -------
        requests.Response
            A JSON object containing a list of dictionaries with the
            compliance status and their counts:
            - ciType: str ("COMPLIANT", "NON-COMPLIANT", "NON-APPLICABLE")
            - count: int

        Example
        -------
        >>> view = 'Node Compliance View'
        >>> compliance_results = calculateView(view)
        >>> for result in compliance_results:
        >>>     print(result['ciType'], result['count'])
        >>>
        >>> COMPLIANT 484
        >>> NON-COMPLIANT 310
        """
        encoded_view = quote(view)
        url = f'{self.client.base_url}/uiserver/modeling/views/{encoded_view}'
        return self.client.session.post(url)

    def getComplainceViews(self):
        """
        Retrieves the valid compliance views based on policies that exist
        in a UCMDB system.

        This method makes a GET request to the UCMDB server to fetch a list
        of compliance views.

        Parameters
        ----------
        None

        Returns
        -------
        requests.Response
            A JSON object containing a list of dictionaries, each
            representing a compliance view with the following keys:
            - name: str
            - baseViewName: str
            - policyQueries: list of str

        Example
        -------
        >>> compliance_views = getComplainceViews()
        >>> for view in compliance_views:
        >>>     print(view['name'], view['baseViewName'], view['policyQueries'])
        >>>
        >>> Certificates must use https Node with WebServer ['Certificates must use https']
        >>> Kubernetes statefulset must have pod Kubernetes StatefulSet ['Kubernetes statefulset must have pod']
        """  # noqa: E501
        url = f'{self.client.base_url}/policy/complianceViews'
        return self.client.session.get(url)

    def getChunkForPath(self, execution_id, chunk, status_type=ComplianceStatus.NON_COMPLIANT):
        """
        Retrieves a specific data chunk for a given path (status) from the UCMDB server.

        This method makes a POST request to the UCMDB server to retrieve
        a specific chunk of compliance data.

        Parameters
        ----------
        execution_id : str
            The ID of the view execution.
        chunk : int
            The number of the chunk to retrieve.
        status_type : ComplianceStatus or str, optional
            The compliance status ("COMPLIANT", "NON-COMPLIANT", "NON-APPLICABLE").
            Default is ComplianceStatus.NON_COMPLIANT.

        Returns
        -------
        requests.Response
            Response object containing the requested compliance data chunk.

        Example
        -------
        >>> from ucmdb_rest.policies import ComplianceStatus
        >>> execution_id = 'example_execution_id'
        >>> chunk = 1
        >>> response = getChunkForPath(execution_id, chunk, ComplianceStatus.NON_COMPLIANT)
        >>> print(response.status_code)
        >>> 200
        """
        status_value = status_type.value if hasattr(status_type, 'value') else status_type
        body = {
            "viewExecutionId": execution_id,
            "path": [{
                "pathElementId": status_value,
                "pathElementType": status_value
            }],
            "chunkNumber": chunk
        }
        url = f'{self.client.base_url}/policy/chunkForPath?chunkSize=300'
        return self.client.session.post(url, json=body)

    def getAllResultsForPath(self, execution_id, status_type=ComplianceStatus.NON_COMPLIANT):
        """
        Automatically iterates through all chunks for a specific status 
        and returns one flat list of results.

        This method handles the pagination logic of the UCMDB server by 
        first determining the number of chunks and then sequentially 
        retrieving and aggregating them into a single list.

        Parameters
        ----------
        execution_id : str
            The ID of the view execution (viewResultId).
        status_type : ComplianceStatus or str, optional
            The compliance status to retrieve ("COMPLIANT", 
            "NON-COMPLIANT", "NON-APPLICABLE"). 
            Default is ComplianceStatus.NON_COMPLIANT.

        Returns
        -------
        list
            A flat list of dictionaries representing the compliance results,
            aggregated from all available chunks.

        Example
        -------
        >>> from ucmdb_rest.policies import ComplianceStatus
        >>> exec_id = 'eyJ0eXAiOiJKV1...'
        >>> results = getAllResultsForPath(exec_id, ComplianceStatus.NON_COMPLIANT)
        >>> print(len(results))
        450
        """
        all_results = []
        status_value = status_type.value if hasattr(status_type, 'value') else status_type
        
        payload = {
            "viewExecutionId": execution_id,
            "path": [{
                "pathElementId": status_value,
                "pathElementType": status_value
            }]
        }
        count_res = self.getNumberOfElements(payload)
        
        if count_res.status_code != 200:
            return []

        data = count_res.json()
        num_chunks = data.get('numberOfChunks', 0)

        for i in range(1, num_chunks + 1):
            chunk_res = self.getChunkForPath(execution_id, i, status_type)
            if chunk_res.status_code == 200:
                chunk_data = chunk_res.json()
                items = chunk_data if isinstance(chunk_data, list) else chunk_data.get('cis', [])
                all_results.extend(items)
        
        return all_results

    def getNumberOfElements(self, payload):
        """
        Retrieves the number of elements for a specified path from the UCMDB
        server.

        This method makes a POST request to the UCMDB server to retrieve the
        number of elements for a specified path.

        Parameters
        ----------
        payload : dict
            The payload containing the necessary data for the request.

        Returns
        -------
        requests.Response
            Response object containing the number of elements for the specified
            path.

        Example
        -------
        >>> payload = {'data': 'example_data'}
        >>> response = getNumberOfElements(payload)
        >>> print(response.status_code)
        >>> 200
        """
        url = f'{self.client.base_url}/uiserver/modeling/views/result/numberOfElementsForPath'
        return self.client.session.post(url,json=payload)

    def getPolicies(self):
        """
        Retrieves the valid policies that exist in a UCMDB system.

        This method makes a GET request to the UCMDB server to fetch a list
        of valid policies.

        Parameters
        ----------
        None

        Returns
        -------
        requests.Response
            A JSON object containing a list of dictionaries, each
            representing a policy with the following keys:
            - name: str
            - path: str
            - simplePolicy: bool

        Example
        -------
        >>> policies = getPolicies()
        >>> for policy in policies:
        ...     print(policy['name'], policy['path'], policy['simplePolicy'])
        ...
        Certificates must use https Query/Policy/Security True
        Kubernetes must have pod Query/Policy/Cloud Compliance/Kubernetes False
        """
        url = f'{self.client.base_url}/policy/policies'
        return self.client.session.get(url)
        
    def getSpecificComplianceView(self, cv):
        """
        Retrieves the result of a specific compliance report.

        This method makes a GET request to the UCMDB server to fetch the details
        of a specific compliance view.

        Parameters
        ----------
        cv : str
            The name of the compliance view.

        Returns
        -------
        requests.Response
            A JSON object containing details of the specified compliance view,
            including:
            - name: str
            - baseViewName: str
            - policyQueries: list of str

        Example
        -------
        >>> cv = 'Nodes with Discovery Probe'
        >>> compliance_view = getSpecificComplianceView(cv)
        >>> print(compliance_view['name'])
        >>> 'Nodes with Discovery Probe'

        Notes
        -----
        The quote function is used to properly encode the compliance view
        name, ensuring that it can be safely used as part of a URL.
        """
        the_name = quote(cv)
        url = f'{self.client.base_url}/policy/complianceView/{the_name}'
        return self.client.session.get(url)