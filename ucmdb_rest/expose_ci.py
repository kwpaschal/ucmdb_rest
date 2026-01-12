# -*- coding: utf-8 -*-
"""
UCMDB Expose CI Service

This module provides a powerful searching and data extraction interface. 
It allows users to define complex filters, select specific layout attributes, 
 and retrieve bulk CI data without needing a pre-defined TQL.

Exposed Methods:
    getInformation, search_by_label
"""

class ExposeCI:
    def __init__(self, client):
        """
        Initialize the service with a reference to the main level UCMDB client
        """
        self.client = client

    def getInformation(self, json_to_expose):
        '''
        Parameters
        ----------
        json_to_expose : dict
            A dictionary defining the CI Type, attribute layout, 
            sorting, and filtering conditions.
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
                            "value": "name_to_get",
                            "filteringAttributeCondOperator": "Like"
                        }
                    ]
                }
            }

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
        url = f'{self.client.base_url}/exposeCI/getInformation'
        return self.client.session.post(url, json=json_to_expose)

def search_by_label(self, label_pattern, ci_type="node", operator="LIKE", layout=None):
        """
        A flexible helper to find CIs of any type based on their display label.

        Parameters
        ----------
        label_pattern : str
            The string to search for.
        ci_type : str, optional
            The UCMDB CI Type (e.g., 'node', 'ip_address', 'business_service'). 
            Default is 'node'.
        operator : str, optional
            The filtering operator (e.g., 'LIKE', 'EQUAL'). Default is 'LIKE'.
        layout : list of str, optional
            Specific attributes to return. If None, defaults to 
            ['display_label', 'name', 'global_id'].
        """
        if layout is None:
            layout = ["display_label", "name", "global_id"]

        payload = {
            "type": ci_type,
            "layout": layout,
            "includeSubtypes": "true",
            "filtering": {
                "logicalOperator": "and",
                "conditions": [
                    {
                        "column": "display_label",
                        "value": label_pattern,
                        "filteringAttributeCondOperator": operator
                    }
                ]
            }
        }
        url = f'{self.client.base_url}/exposeCI/getInformation'
        return self.client.session.post(url, json=payload)