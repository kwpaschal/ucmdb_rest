# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:11:06 2024

@author: kpaschal
"""

import requests

from .utils import _url
from . import config

def exposeCI(token, udserver, json_to_expose, verification_flag=False):
    print(json_to_expose)
    '''
    Parameters
    ----------
    token : dict
        Authentication token created by calling the function 
        'createHeaders' with arguments of ucmdb_user, ucmdb_pass, 
        and ucmdb_server.
    udserver : str
        UCMDB server hostname or IP address.
    json_to_expose : dict
        This is a representation of a pattern of CIs to expose. For example:
        {
            "type": "running_software",
            "layout": [
                "display_label",
                "discovered_product_name",
                "global_id",
                "version",
                "mf_version"
            ],
            "includeSubtypes": "false",
            "sortBy": [
                {
                    "attribute": "version",
                    "order": "DESC"
                }
            ],
            "filtering": {
                "logicalOperator": "and",
                "conditions": [
                    {
                        "column": "discovered_product_name",
                        "value": name_to_get,
                        "filteringAttributeCondOperator": "Like"
                    }
                ]
            }
        }
    verification_flag : bool, optional
        Flag to verify the SSL certificate (default is False).

    Returns
    -------
    requests.Response
        Can be converted to a list of dictionaries where each dictionary
        is representative of an element requested. For example:
        [
            {
                "ucmdbId": "4e8b850822c83fdb975dc2bf899c7686",
                "globalId": "4e8b850822c83fdb975dc2bf899c7686",
                "type": "running_software",
                "properties": {
                    "display_label": "OpenText UCMDB Server (bra03ucm02)",
                    "discovered_product_name": "OpenText UCMDB Server",
                    "global_id": "4e8b850822c83fdb975dc2bf899c7686",
                    "version": "10.22.CUP3"
                },
                "attributesDisplayNames": null,
                "attributesQualifiers": null,
                "attributesType": null,
                "classDefinition": null,
                "displayLabel": null
            }
        ]

    '''
    return requests.post(_url(udserver, '/exposeCI/getInformation'),
                        headers=token, json=json_to_expose,
                        verify=verification_flag)