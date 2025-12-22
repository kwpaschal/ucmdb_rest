# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 14:49:33 2024

@author: kpaschal

This python 3 library contains methods relating to UCMDB compliance views
"""
import requests
from urllib.parse import quote

from .utils import _url
from . import config

def calculateComplianceView(token, udserver, myDict):
    """
    Calculates compliance based on provided data.

    This method makes a POST request to the UCMDB server to calculate
    compliance based on the provided data.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    myDict : dict
        Data to be used for compliance calculation.

    Returns
    -------
    requests.Response
        Response object from the UCMDB server.

    Example
    -------
    >>> token = 'example_token'
    >>> udserver = 'example_ucmdb_server'
    >>> my_dict = {'data': 'example_data'}
    >>> response = calculateComplianceView(token, udserver, my_dict)
    >>> print(response.status_code)
    200
    """
    return requests.post(_url(udserver, '/policy/calculate?chunckSize=300'),
                         json=myDict, headers=token, verify=config.get_verify_ssl())

def calculateView(token, udserver, view):
    """
    Calculates a compliance view based on policies that exist in a
    UCMDB system.

    This method makes a POST request to the UCMDB server to calculate a
    compliance view. The results are a list of dictionaries containing
    the COMPLIANT, NON-COMPLIANT, and NON-APPLICABLE values. The view
    must be from the list created by getComplainceViews.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        The UCMDB server hostname or IP address that is valid for DNS
        resolution.
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
    >>> headers = createHeaders('username', 'password', 'ucmdb_server')
    >>> udserver = '127.0.0.1'
    >>> view = 'Node Compliance View'
    >>> compliance_results = calculateView(headers, udserver, view)
    >>> for result in compliance_results:
    >>>     print(result['ciType'], result['count'])
    >>>
    >>> COMPLIANT 484
    >>> NON-COMPLIANT 310
    """
    encoded_view = quote(view)
    return requests.post(_url(udserver, '/uiserver/modeling/views/' + encoded_view),
                         headers=token, verify=config.get_verify_ssl(), json={})

def getComplainceViews(token, udserver):
    """
    Retrieves the valid compliance views based on policies that exist
    in a UCMDB system.

    This method makes a GET request to the UCMDB server to fetch a list
    of compliance views.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 'createHeaders'
        with arguments of ucmdb_user, ucmdb_pass, and ucmdb_server.
    udserver : str
        The UCMDB server hostname or IP address that is valid for DNS
        resolution.

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
    >>> token = createHeaders('username', 'password', 'ucmdb_server')
    >>> udserver = '127.0.0.1'
    >>> compliance_views = getComplainceViews(token, udserver)
    >>> for view in compliance_views:
    >>>     print(view['name'], view['baseViewName'], view['policyQueries'])
    >>>
    >>> Certificates must use https Node with WebServer ['Certificates must use https']
    >>> Kubernetes statefulset must have pod Kubernetes StatefulSet ['Kubernetes statefulset must have pod']
    """
    return requests.get(_url(udserver, '/policy/complianceViews'),
                        headers=token, verify=config.get_verify_ssl())

def getNonCompliant(token, udserver, execution_id, chunk):
    """
    Retrieves non-compliant data chunks from the UCMDB server.

    This method makes a POST request to the UCMDB server to retrieve
    non-compliant data chunks.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    execution_id : str
        The ID of the view execution.
    chunk : int
        The number of the chunk to retrieve.

    Returns
    -------
    requests.Response
        Response object containing the requested non-compliant data chunk.

    Example
    -------
    >>> token = 'example_token'
    >>> udserver = 'example_ucmdb_server'
    >>> execution_id = 'example_execution_id'
    >>> chunk = 1
    >>> response = getNonCompliant(token, udserver, execution_id, chunk)
    >>> print(response.status_code)
    >>> 200
    """
    body = {
        "viewExecutionId": execution_id,
        "path": [{
            "pathElementId": "NON-COMPLIANT",
            "pathElementType": "NON-COMPLIANT"
        }],
        "chunkNumber": chunk
    }
    return requests.post(_url(udserver, '/policy/chunkForPath?chunkSize=300'),
                         headers=token, json=body, verify=config.get_verify_ssl())

def getNumberOfElements(token, udserver, payload):
    """
    Retrieves the number of elements for a specified path from the UCMDB
    server.

    This method makes a POST request to the UCMDB server to retrieve the
    number of elements for a specified path.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 'createHeaders'
        with arguments of ucmdb_user, ucmdb_pass, and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    payload : dict
        The payload containing the necessary data for the request.

    Returns
    -------
    requests.Response
        Response object containing the number of elements for the specified
        path.

    Example
    -------
    >>> token = 'example_token'
    >>> udserver = 'example_ucmdb_server'
    >>> payload = {'data': 'example_data'}
    >>> response = getNumberOfElements(token, udserver, payload)
    >>> print(response.status_code)
    >>> 200
    """
    return requests.post(_url(udserver, '/uiserver/modeling/views/result/numberOfElementsForPath'),
                         headers=token, json=payload, verify=config.get_verify_ssl())


def getPolicies(token, udserver):
    """
    Retrieves the valid policies that exist in a UCMDB system.

    This method makes a GET request to the UCMDB server to fetch a list
    of valid policies.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 'createHeaders'
        with arguments of ucmdb_user, ucmdb_pass, and ucmdb_server.
    udserver : str
        The UCMDB server hostname or IP address that is valid for DNS
        resolution.

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
    >>> token = createHeaders('username', 'password', 'ucmdb_server')
    >>> udserver = '127.0.0.1'
    >>> policies = getPolicies(token, udserver)
    >>> for policy in policies:
    ...     print(policy['name'], policy['path'], policy['simplePolicy'])
    ...
    Certificates must use https Query/Policy/Security True
    Kubernetes must have pod Query/Policy/Cloud Compliance/Kubernetes False
    """
    return requests.get(_url(udserver, '/policy/policies'),
                        headers=token, verify=config.get_verify_ssl())
    
def getSpecificComplianceView(token, udserver, cv):
    """
    Retrieves the result of a specific compliance report.

    This method makes a GET request to the UCMDB server to fetch the details
    of a specific compliance view.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        The UCMDB server hostname or IP address that is valid for DNS
        resolution.
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
    >>> token = createHeaders('username', 'password', 'ucmdb_server')
    >>> udserver = '127.0.0.1'
    >>> cv = 'Nodes with Discovery Probe'
    >>> compliance_view = getSpecificComplianceView(token, udserver, cv)
    >>> print(compliance_view['name'])
    >>> 'Nodes with Discovery Probe'

    Notes
    -----
    The quote function is used to properly encode the compliance view
    name, ensuring that it can be safely used as part of a URL.
    """
    the_name = quote(cv)
    return requests.get(_url(udserver, '/policy/complianceView/' + the_name),
                        headers=token, verify=config.get_verify_ssl())