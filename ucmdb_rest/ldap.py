# -*- coding: utf-8 -*-
"""
UCMDB LDAP Service

This module provides methods to retrieve and inspect the LDAP integration 
settings used by UCMDB for user authentication and group mapping.

Exposed Methods:
    getLDAPSettings
"""

class RetrieveLDAP:
    def __init__(self, client):
        """
        Initialize the service with a reference to the main level UCMDB client
        """
        self.client = client

    def getLDAPSettings(self):
        """
        Retrieves the full LDAP configuration from the UCMDB server.

        This includes connection URLs, service account details (masked), 
        user/group search filters, and attribute mappings.

        Returns
        -------
        requests.Response
            A JSON array containing dictionaries for each configured 
            LDAP repository.
            
        Example Response Structure:
        ---------------------------
        [
            {
                "connection": {"url": "ldap://...", "searchUser": "..."},
                "user": {"userClass": "user", "uniqueIdAttribute": "employeeID"},
                "group": {"groupClass": "group", "memberAttribute": "member"}
            }
        ]
        """
        url = f'{self.client.base_url}/ldap/settings'
        return self.client.session.get(url)