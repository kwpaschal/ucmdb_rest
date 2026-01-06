"""
Created on Wed Jun  5 14:33:54 2024

@author: kpaschal

This library contains imports for topology methods.
"""

class Topology:
    def __init__(self, client):
        """
        Initialize the service with a reference to the main level UCMDB client
        """
        self.client = client

    def get_all_view_results(self, view_name, chunkSize=10000):
        """
        Runs a view and automatically fetches all chunks, returning a combined result.
        """
        response = self.runView(view_name, chunkSize=chunkSize)
        response.raise_for_status()
        
        data = response.json()
        
        all_cis = data.get('cis') or []
        all_relations = data.get('relations') or []
        
        res_id = data.get('queryResultId')
        num_chunks = data.get('numberOfChunks', 0)
        
        if not res_id:
            return {"cis": all_cis, "relations": all_relations}
        
        for i in range(1, num_chunks + 1):
            chunk_resp = self.getChunk(res_id, i)
            chunk_resp.raise_for_status()
            chunk_data = chunk_resp.json()
            
            new_cis = chunk_data.get('cis') or []
            new_relations = chunk_data.get('relations') or []
            
            all_cis.extend(new_cis)
            all_relations.extend(new_relations)
                
        return {"cis": all_cis, "relations": all_relations}

    def getChunk(self, res_id, index):
        '''
        This method retrieves the values in each chunk (index).

        Parameters
        ----------
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
        url = f'{self.client.base_url}/topology/result/{res_id}/{index}'
        return self.client.session.get(url)

    def getChunkForPath(self, state, execution_id, chunk):
        """
        Retrieves a chunk of data for a specific path from the UCMDB server.

        This method makes a POST request to the UCMDB server to retrieve a 
        chunk of data for a specific path.

        Parameters
        ----------
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
        """
        body = {
            "viewExecutionId": execution_id,
            "path": [{"pathElementId": state, "pathElementType": state}],
            "chunkNumber": chunk
        }
        url = f'{self.client.base_url}/uiserver/modeling/views/result/chunkForPath'
        return self.client.session.post(url, json=body)

    def queryCIs(self, query):
        '''
        Retrieves the result of a query defined in UCMDB via a REST API POST 
        call.

        Parameters
        ----------
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
        url = f'{self.client.base_url}/topologyQuery'
        return self.client.session.post(url, json=query)

    def runView(self, view, includeEmptyLayout=False, chunkSize=10000):
        '''
        Retrieves the result of a view defined in UCMDB via a REST API POST 
        call

        Parameters
        ----------
        view : str
            Name of a view on the UCMDB server.
        includeEmptyLayout : bool
            Should empty layouts be shown? Default is False.
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
        url = f'{self.client.base_url}/topology?includeEmptyLayoutProperties={includeEmptyLayout}&chunkSize={chunkSize}'
        return self.client.session.post(url, json=view)