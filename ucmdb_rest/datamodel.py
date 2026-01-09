# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:05:19 2024

@author: kpaschal
"""

import base64


class DataModel:
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
        Adds a given bulk of CIs which are defined outside this
        method.

        Parameters
        ----------
        ciToCreate : dict
            A dictionary representing CIs to add. For example:
            {
            "cis": [
                    {
                    "ucmdbId": "1",
                    "type": "node",
                    "properties": {"name":"Test6",
                                    "os_family":"windows"}
                    },{
                    "ucmdbId": "2",
                    "type": "ip_address",
                    "properties": {"name":"100.100.100.1"}
                    },{
                    "ucmdbId": "4",
                    "type": "running_software",
                    "properties": {
                        "discovered_product_name":
                        "my software"}
                    }
                ],
                "relations": [
                    {
                    "ucmdbId":"3",
                    "type": "containment",
                    "end1Id": 1,
                    "end2Id": 2,
                    "properties": {}
                    },{
                    "ucmdbId": "5",
                    "type": "composition",
                    "end1Id": 1,
                    "end2Id": 4,
                    "properties": {}
                    }
                ]
            }
        isGlobalId : bool, optional
            Is there a global ID in the payload to use?
            The default is False.
        forceTemporaryID : bool, optional
            Is there a temporary object ID in the payload?
            The default is False.
        verify_flag : bool, optional
            Should we verify the SSL certificate of the server?
            The default is False.
        ignoreExisting : bool, optional
            Should we ignore an existing CI when trying to create one?
            The default is False. This could result in an empty map,
            such as:
            {
            "addedCis": [],
            "removedCis": [],
            "updatedCis": [],
            "ignoredCis": []
            }
        returnIdsMap : bool, optional
            Should we return an ID Map? The default is False.
            The output is different if this is True:
            {
            "addedCis": [],
            "removedCis": [],
            "updatedCis": [],
            "ignoredCis": [
                "44c93b1d0230dd02b013364a7b8c635f",
                "46861bedaa49a57c8ded7bd5598063d1",
                "425c6932d1c77461b334820a5f11ba06",
                "49207844d429e0aa8b12deebb2f02a49",
                "4c08d336b05421a1ae48c067951f9248"
            ],
            "idsMap": {
                "1": "44c93b1d0230dd02b013364a7b8c635f",
                "2": "46861bedaa49a57c8ded7bd5598063d1",
                "3": "425c6932d1c77461b334820a5f11ba06",
                "4": "49207844d429e0aa8b12deebb2f02a49",
                "5": "4c08d336b05421a1ae48c067951f9248"
            }
            }
            This shows that in our input the thing referred to as 1
            is now the global ID: 44c93b1d0230dd02b013364a7b8c635f
        ignoreWhenCantIdentify : bool, optional
            Should we ignore what cannot be identified, or throw an
            error? The default is False.

        Returns
        -------
        requests.Response
            This is a dictionary of what was added, removed, updated
            or ignored.
            {
            "addedCis": [],
            "removedCis": [],
            "updatedCis": [],
            "ignoredCis": [
                "44c93b1d0230dd02b013364a7b8c635f",
                "46861bedaa49a57c8ded7bd5598063d1",
                "425c6932d1c77461b334820a5f11ba06",
                "49207844d429e0aa8b12deebb2f02a49",
                "4c08d336b05421a1ae48c067951f9248"
            ]
            }

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
        Deletes a CI by its ID by making a delete request via the
        REST API.

        Parameters
        ----------
        id_to_delete : str
            This is the global or local UCMDB ID.
        isGlobalId : bool, optional
            Is the ID a global ID? The default is False.
        verify_flag : bool, optional
            Should the SSL certificate of the UCMDB server be verified?
            The default is False.

        Returns
        -------
        requests.Response
            A dictionary describing the results. For example:
            {
                "addedCis": [],
                "removedCis": [
                    "44c93b1d0230dd02b013364a7b8c635f"
                ],
                "updatedCis": [],
                "ignoredCis": []
            }

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
        Issues a REST API get call to show the identification rule for a CI Type

        Parameters
        ----------
        cit : str, optional
            CI type name to retrieve. The default is 'node'.
        verify_flag : bool, optional
            Check the SSL certificate of the UCMDB server? The default is False.

        Returns
        -------
        requests.Response
            The response object containing the class model information.
            To get the decoded identification rule XML, use:
            ```python
            response = retrieveIdentificationRule('node')
            data = response.json()
            xml = convertFromBase64(data["identification"]["ruleXml"])
            ```

            Example XML format:
                <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <identification-config type="location" description="Location is identified by a
                  combination of (Name, LocationType) or (Name, CloudLocationType). Two similarly
                   identified locations will be considered different entities if they are contained
                   in different locations.">
                    <identification-criteria>
                        <identification-criterion>
                            <attribute-condition attributeName="name" includeNullValue="false"
                             conditionType="approveAndContradict" matchNameOnly="false"/>
                            <attribute-condition attributeName="location_type"
                            includeNullValue="false" conditionType="approveAndContradict"
                             matchNameOnly="false"/>
                        </identification-criterion>
                        <identification-criterion>
                            <attribute-condition attributeName="name" includeNullValue="false"
                             conditionType="approveAndContradict" matchNameOnly="false"/>
                            <attribute-condition attributeName="cloud_location_type"
                              includeNullValue="false" conditionType="approveAndContradict"
                                matchNameOnly="false"/>
                        </identification-criterion>
                    </identification-criteria>
                    <match>
                        <verification-criteria>
                            <verification-criterion>
                                <connected-ci-condition ciType="location" linkType="containment"
                                  isDirectionForward="false" conditionType="approveAndContradict">
                                    <overlap-fixed-operator number-of-matches="1"/>
                                </connected-ci-condition>
                            </verification-criterion>
                        </verification-criteria>
                    </match>
                </identification-config>

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
