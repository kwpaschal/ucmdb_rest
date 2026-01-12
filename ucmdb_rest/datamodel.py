# -*- coding: utf-8 -*-
"""
UCMDB Data Model and Class Model Service

This module provides an interface to the UCMDB Object Model. It is divided 
into two primary functional areas:

1. Data Model (Instances): 
   Methods for CRUD operations on CIs and Relationships (addCIs, updateCI, 
   deleteCIs).
   
2. Class Model (Metadata): 
   Methods for inspecting CI Type definitions, attributes, and identification 
   rules (getCIProperties, retrieveIdentificationRule).

Exposed Methods:
    addCIs, convertFromBase64, deleteCIs, getCIProperties, 
    retrieveIdentificationRule, updateCI

Usage:
    # Create a new CI
    new_ci = {"cis": [{"type": "node", "properties": {"name": "host01"}}]}
    myserver.datamodel.addCIs(new_ci)
"""

import base64


class DataModel:
    """
    Service module for interacting with the UCMDB Class Model and Data Model.

    This module provides methods to create, update, and delete Configuration Items (CIs)
    and Relationships, as well as tools to inspect the CI Type (Class) definitions
    and identification rules.

    Parameters
    ----------
    client : UCMDBServer
        An instance of the primary UCMDB client.
    """
    def __init__(self, client):
        """
        Initialize the service with a reference to the main level UCMDB client
        """
        self.client = client

    @staticmethod
    def convertFromBase64(stringToDecode):
        """
        The function takes a Base64-encoded string, converts it to bytes, decodes
        it using Base64 decoding, and then converts the resulting bytes back into
        a UTF-8 string, which is then returned.

        Parameters
        ----------
        stringToDecode: base64 string
            A Base 64 encoded string
        Returns
        -------
        decoded_string: str
            A UTF-8 string
        """
        base64_bytes = stringToDecode.encode("utf-8")
        sample_string_bytes = base64.b64decode(base64_bytes)
        decoded_string = sample_string_bytes.decode("utf-8")
        return decoded_string

    def addCIs(
        self,
        ciToCreate,
        isGlobalId=False,
        forceTemporaryID=False,
        ignoreExisting=False,
        returnIdsMap=False,
        ignoreWhenCantIdentify=False,
    ):
        """
        Adds or updates a bulk collection of CIs and Relationships.

        Parameters
        ----------
        ciToCreate : dict
            A dictionary defining the CIs and relations.
            Example:
            {
                "cis": [{"ucmdbId": "1", "type": "node", "properties": {"name": "Test"}}],
                "relations": [{"type": "containment", "end1Id": "1", "end2Id": "2"}]
            }
        isGlobalId : bool, optional
            Whether IDs in the payload are global UCMDB IDs. Default is False.
        forceTemporaryID : bool, optional
            Whether to treat provided IDs as temporary identifiers. Default is False.
        ignoreExisting : bool, optional
            If True, existing CIs will not be updated. Default is False.
        returnIdsMap : bool, optional
            If True, returns a mapping of temporary IDs to actual UCMDB IDs. Default is False.
        ignoreWhenCantIdentify : bool, optional
            If True, skips CIs that do not match identification rules instead of failing.
            Default is False.

        Returns
        -------
        requests.Response
            A response containing lists of added, removed, updated, or ignored IDs.
        """
        query_params = {
            "isGlobalId": str(isGlobalId).lower(),
            "forceTemporaryId": str(forceTemporaryID).lower(),
            "ignoreExisting": str(ignoreExisting).lower(),
            "returnIdsMap": str(returnIdsMap).lower(),
            "ignoreWhenCantIdentify": str(ignoreWhenCantIdentify).lower(),
        }
        url = f"{self.client.base_url}/dataModel"
        return self.client.session.post(url, json=ciToCreate, params=query_params)

    def deleteCIs(self, id_to_delete, isGlobalId=False):
        """
        Deletes a specific CI by its ID.

        Parameters
        ----------
        id_to_delete : str
            The UCMDB ID (local or global) to delete.
        isGlobalId : bool, optional
            Set to True if the ID provided is a Global ID. Default is False.

        Returns
        -------
        requests.Response
            A summary of the deletion result.
        """
        url = f"{self.client.base_url}/dataModel/ci/{id_to_delete}"
        params = {"isGlobalId": str(isGlobalId).lower()}
        return self.client.session.delete(url, params=params)

    def getClass(self, CIT):
        """
        Retrieves the definition of a class (CI Type) from the UCMDB server.

        This method makes a GET request to the UCMDB server to fetch the
        definition of the specified class.

        Parameters
        ----------
        CIT : str
            The class name (e.g., "node").
        verify : bool
            Verify the SSL certificate or not (default is False)

        Returns
        -------
        requests.Response
            A JSON object describing the CI Type, with attributes such as:
            - name
            - displayName
            - superClass
            - description
            - allAttributes (list of dictionaries, each representing an
                            attribute)
            - classAttributes (list of dictionaries, each representing an
                            attribute defined in this class)
            - iconName
            - children
            - parents
            - qualifiers
            - classType
            - classQualifiers
            - defaultLabel
            - validLinks
            - identification (dictionary with identification details)
            - editable
            - scope
            - deletable
            - createdByFactory
            - modifiedByUser

        Example
        -------
        >>> CIT = 'node'
        >>> class_def = getClass(CIT)
        >>> print(class_def['name'])
        'node'
        """
        url = f"{self.client.base_url}/classModel/citypes/{CIT}"
        return self.client.session.get(url)

    def retrieveIdentificationRule(self, cit="node"):
        """
        Retrieves the XML identification rule for a specific CI Type.

        Parameters
        ----------
        cit : str, optional
            The CI Type name. Default is 'node'.

        Returns
        -------
        requests.Response
            The response containing the Base64 encoded 'ruleXml'.
            
        Examples
        --------
        >>> response = model.retrieveIdentificationRule('node')
        >>> rule_b64 = response.json()["identification"]["ruleXml"]
        >>> xml = model.convertFromBase64(rule_b64)
        """
        url = f"{self.client.base_url}/classModel/citypes/{cit}?withAffectedResources=false"
        return self.client.session.get(url)

    def updateCI(self, id_to_update, update_ci):
        """
        Updates a CI by ID via a PUT REST API call.

        Parameters
        ----------
        id_to_update : str
            The global CI identifier (or LOCAL CI identifier).
        update_ci : dict
            A dictionary containing the update.
        verify_flag : bool, optional
            Should SSL be verified? The default is False.

        Returns
        -------
        requests.Response
            The results of the update. For example:
            {
                "addedCis": [],
                "removedCis": [],
                "updatedCis": [
                    "44c93b1d0230dd02b013364a7b8c635f"
                ],
                "ignoredCis": []
            }
        """
        url = f"{self.client.base_url}/dataModel/ci/{id_to_update}"
        return self.client.session.put(url, json=update_ci)
