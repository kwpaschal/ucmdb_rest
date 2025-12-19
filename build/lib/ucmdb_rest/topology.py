"""
Created on Wed Jun  5 14:33:54 2024

@author: kpaschal

This library contains imports for topology methods.
"""
import requests
from .utils import _url


def getChunk(token, udserver, res_id, index):
    '''
    This method retrieves the values in each chunk (index).

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    res_id : str
        The result ID from the topology call.
    index : int
        Which chunk to get.

    Returns
    -------
    requests.Response
        Can be converted to a dictionary containing the CIs and relations. For example:
            {
              "cis": [
                {
                  "ucmdbId": "4fc4d26b423c52bd99c3586017fd55e7",
                  "globalId": null,
                  "type": "nt",
                  "properties": {
                    "display_label": "pue01vm0040"
                  },
                  "attributesDisplayNames": null,
                  "attributesQualifiers": null,
                  "attributesType": null,
                  "classDefinition": null,
                  "displayLabel": null,
                  "label": "Windows"
                },
                {
                  "ucmdbId": "4fe8814b30be8ca4aeedcf1e4323fa62",
                  "globalId": null,
                  "type": "nt",
                  "properties": {
                    "display_label": "pue01vm1278"
                  },
                  "attributesDisplayNames": null,
                  "attributesQualifiers": null,
                  "attributesType": null,
                  "classDefinition": null,
                  "displayLabel": null,
                  "label": "Windows"
                },
                {
                  "ucmdbId": "4fee7d96a41be2f48f7fd343e815b6de",
                  "globalId": null,
                  "type": "nt",
                  "properties": {
                    "display_label": "bra03pc78"
                  },
                  "attributesDisplayNames": null,
                  "attributesQualifiers": null,
                  "attributesType": null,
                  "classDefinition": null,
                  "displayLabel": null,
                  "label": "Windows"
                }
              ],
              "relations": []
            }
    '''
    return requests.get(
        _url(udserver, f'/topology/result/{res_id}/{index}'),
        headers=token,
        verify=False
    )

def getChunkForPath(token: dict, udserver: str, state: str, execution_id: str, 
                    chunk: int):
    """
    Retrieves a chunk of data for a specific path from the UCMDB server.

    This method makes a POST request to the UCMDB server to retrieve a 
    chunk of data for a specific path.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    state : str
        The path element ID.
    execution_id : str
        The ID of the view execution.
    chunk : int
        The number of the chunk to retrieve.

    Returns
    -------
    requests.Response
        Response object containing the requested chunk of data.

    Example
    -------
    >>> token = 'example_token'
    >>> udserver = 'example_ucmdb_server'
    >>> state = 'example_state'
    >>> execution_id = 'example_execution_id'
    >>> chunk = 1
    >>> response = getChunkForPath(token, udserver, state, execution_id, 
                                   chunk)
    >>> print(response.status_code)
    200
    """
    body = {
        "viewExecutionId": execution_id,
        "path": [{"pathElementId": state, "pathElementType": state}],
        "chunkNumber": chunk
    }
    return requests.post(
        _url(udserver, '/uiserver/modeling/views/result/chunkForPath'),
        headers=token, 
        json=body, 
        verify=False
    )


def queryCIs(token, udserver, query, verify_flag=False):
    '''
    Retrieves the result of a query defined in UCMDB via a REST API POST 
    call.

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    query : dict
        JSON describing the query. For example:
            {
                "nodes": [
                    {
                        "type": "node",
                        "queryIdentifier": "node",
                        "visible": "true",
                        "includeSubtypes": "true",
                        "layout": ["display_label"],
                        "attributeConditions": [],
                        "linkConditions": [],
                        "ids": []
                    }
                ],
                "relations": []
            }
    verify_flag : bool, optional
        Should we verify the SSL Certificate in the UCMDB server? The 
        default is False.

    Returns
    -------
    requests.Response
        Can be converted to a dictionary containing 2 entries, a list of CIs (dictionaries)
        and a list of relations (also dictionaries). For example:
            {
                "cis": [],
                "relations": []
            }

    '''
    return requests.post(
        _url(udserver, '/topologyQuery'),
        headers=token,
        json=query,
        verify=verify_flag
    )


def runView(token, udserver, view, includeEmptyLayout=False, chunkSize=10000):
    '''
    Retrieves the result of a view defined in UCMDB via a REST API POST 
    call

    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    view : str
        Name of a view on the UCMDB server.
    includeEmptyLayout : Bool
        Should empty layouts be shown?  Default is False.
    chunkSize : int
        The max number of nodes to return in each chunk.

    Returns
    -------
    requests.Response
        Can be converted to a dictionary contains 2 entries, CIs and Relations, each of
        which is a list of dictionaries. For example:
            {
                "cis": [],
                "relations": []
            }

    '''
    url = f'/topology?includeEmptyLayoutProperties={includeEmptyLayout}&'\
          f'chunkSize={chunkSize}'
    return requests.post(
        _url(udserver, url),
        headers=token,
        json=view,
        verify=False
    )

