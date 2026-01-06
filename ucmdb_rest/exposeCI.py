# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:11:06 2024

@author: kpaschal
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

    def search_nodes_by_label(self, label_pattern, operator="LIKE"):
        """Helper to quickly find nodes by display_label."""
        payload = {
            "type": "node",
            "layout": ["display_label", "name", "global_id"],
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
        return self.getInformation(payload)