# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 15:12:48 2024

@author: kpaschal

This python library contains methods dealing with managment zones in the 
UCMDB server.  These zones are CMS UI zones, not UCMDB local client 
management zones.
"""

from urllib.parse import quote

class ManagementZones:
    def __init__(self, client):
        """
        Initialize the service with a reference to the main level UCMDB client
        """
        self.client = client
        # Centralizing the base endpoint to avoid repetition
        self.base_path = f'{self.client.base_url}/discovery/managementzones'
            
    def _get_url(self, zone_id=None):
        """Internal helper to build the URL and handle encoding."""
        if zone_id:
            return f"{self.base_path}/{quote(zone_id)}"
        return self.base_path

    def activateZone(self, zone_id):
        """
        Activates a management zone on the UCMDB server.

        This method makes a PATCH request to the UCMDB server to activate a specific
        management zone.

        Parameters:
        -----------
        zone_id : str
            The ID of the management zone to activate.

        Returns:
        --------
        requests.Response
            Response object confirming the activation of the management zone.

        """
        url = f'{self._get_url(zone_id)}?operation=activate'
        return self.client.session.patch(url)

    def createManagementZone(self, mgmtZone):
        """
        Creates a new management zone on the UCMDB server.

        This method makes a POST request to the UCMDB server to create a 
        new management zone.

        Parameters
        ----------
        mgmtZone : dict
            Dictionary containing the details of the management zone to be 
            created.
            Example:
            {
                "name": "Zone Via REST-API",
                "activated": False,
                "ipRangeProfiles": [
                    {
                        "ipRangeProfileId": "All IP Range Groups"
                    }
                ],
                "discoveryActivities": [
                    {
                        "discoveryProfileId": "Added Thru REST-API",
                        "scheduleProfileId": "Interval 1 Day (Default)",
                        "credentialProfileId": "All Credentials"
                    }
                ]
            }

        Returns
        -------
        requests.Response
            Response object confirming the creation of the management zone.
        """
        return self.client.session.post(self._get_url(), json=mgmtZone)

    def deleteManagementZone(self, zone_id):
        """
        Deletes a management zone from the UCMDB server.

        This method makes a DELETE request to the UCMDB server to delete a specific
        management zone.

        Parameters:
        -----------
        zone_id : str
            The ID of the management zone to delete.

        Returns:
        --------
        requests.Response
            Response object confirming the deletion of the management zone.
        """
        return self.client.session.delete(self._get_url(zone_id))

    def getMgmtZone(self):
        """
        Retrieves management zone details from the UCMDB server.

        This method makes a GET request to the UCMDB server to retrieve management
        zone details.

        Parameters:
        -----------
        None

        Returns:
        --------
        requests.Response
            The response contains a dictionary of items, the items are a list of
            dictionaries including:
                - name : String - The name of the management zone
                - activated :  Boolean - Is the zone active?
                - ipRangeProfiles : A list of dictionaries containing the id
                - discoveryActivities : A list of dictionaries with:
                    - discoveryProfileId : String - Name of the acitivity
                    - scheduleProfileId : String - Name of the interval
                    - credentialProfileId : String - Name of the credentials
                - id : String - Zone name
                - description : String - Description of the discovery
                - triggerSummary : Dictionary - A list of trigger statuses
                
        """
        return self.client.session.get(self._get_url())

    def getSpecificMgmtZone(self, zone_id):
        """
        Retrieves a specific management zone from the UCMDB server.

        This method makes a GET request to the UCMDB server to retrieve a specific
        management zone.

        Parameters:
        -----------
        zone_id : str
            The ID of the management zone to retrieve.

        Returns:
        --------
        requests.Response
            The return is a list of dictionaries with a single entry, 'items'
            Items contains a list of dictionaries
                - name : str
                - Activated: bool
                - IP Range Profiles: list of dicts
                - Discovery Activities: list of dicts
                    - Discovery Profile: str
                    - Schedule Profile: str
                    - Credential Profile: str
                - ID: str
                - Trigger Summary: dict
                    - Total Count: int
                    - Pending Count: int
                    - In Progress Count: int
                    - Success Count: int
                    - Warning Count: int
                    - Error Count: int
                - Result CI Count: int
                - Active Jobs: dict
                    - ASMish: list of str

        """
        return self.client.session.get(self._get_url(zone_id))

    def getStatisticsForZone(self, zone_id):
        """
        Retrieves statistics for a specific management zone from the UCMDB server.

        This method makes a GET request to the UCMDB server to retrieve statistics
        for a specific management zone.

        Parameters:
        -----------
        zone_id : str
            The ID of the management zone for which statistics are requested.

        Returns:
        --------
        requests.Response
            Response object containing the statistics for the specified management zone.
        """
        # This uses a different base (/discovery/results/statistics), so we build it manually
        url = f'{self.client.base_url}/discovery/results/statistics?mzoneId={quote(zone_id)}'
        return self.client.session.get(url)