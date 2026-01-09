# -*- coding: utf-8 -*-
import requests
from requests.exceptions import RequestException

# Importing all services
from .data_flow_management import DataFlowManagement
from .datamodel import DataModel
from .discovery import Discovery
from .expose_ci import ExposeCI
from .integration import Integrations
from .ldap import RetrieveLDAP
from .management_zone import ManagementZones
from .packages import Packages
from .policies import Policies
from .report import Reports
from .settings import Settings
from .system import System
from .topology import Topology


class UCMDBAuthError(Exception):
    """Raised when UCMDB authentication fails."""

    pass


class UCMDBServer:
    def __init__(
        self,
        user,
        password,
        server,
        port=8443,
        protocol="https",
        ssl_validation=False,
        client_context=1,
        classic=True,
    ):
        if classic:
            self.base_url = f"{protocol}://{server}:{port}/rest-api"
        else:
            self.base_url = f"{protocol}://{server}:{port}/ucmdb-server/rest-api"
        self.root_url = f"{protocol}://{server}:{port}"

        # Initialize Session
        self.session = requests.Session()
        self.session.verify = ssl_validation
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )
        self.client_context = client_context

        # Authenticate immediately
        self._authenticate(user, password)

        # Register Service Modules (Standardized naming)
        self.data_flow = DataFlowManagement(self)
        self.data_model = DataModel(self)
        self.policies = Policies(self)
        self.topology = Topology(self)
        self.discovery = Discovery(self)
        self.expose = ExposeCI(self)
        self.integrations = Integrations(self)
        self.ldap = RetrieveLDAP(self)
        self.mgmt_zones = ManagementZones(self)
        self.reports = Reports(self)
        self.settings = Settings(self)
        self.packages = Packages(self)
        self.system = System(self)

    def _authenticate(self, user, password):
        """Internal method to fetch and set the Bearer token."""
        payload = {"username": user, "password": password, "clientContext": self.client_context}

        try:
            response = self.session.post(f"{self.base_url}/authenticate", json=payload)

            if response.status_code == 200:
                token = response.json().get("token")
                self.session.headers.update({"Authorization": f"Bearer {token}"})
            else:
                raise UCMDBAuthError(f"Auth Failed ({response.status_code}): {response.text}")
        except RequestException as e:
            raise ConnectionError(f"Failed to connect to UCMDB at {self.base_url}: {e}")
