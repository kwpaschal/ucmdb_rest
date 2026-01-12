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
    """
    The primary interface for interacting with the UCMDB REST API.

    This class manages the lifecycle of a UCMDB session, including 
    authentication, token refreshment, and provides access to specialized 
    sub-modules for topology, discovery, and policies.

    Parameters
    ----------
    server : str
        The hostname or IP address of the UCMDB server.
    user : str
        The username for authentication.
    password : str
        The password for authentication.
    port : int, optional
        The REST API port (default is 8443).
    protocol : str, optional
        The connection protocol, 'http' or 'https' (default is 'https').
    ssl_validation : bool, optional
        Whether to verify the server's SSL certificate (default is False).
    client_context : int, optional
        The UCMDB client context ID (default is 1).
    classic : bool, optional
        Whether UCMDB is installed in classic or containerized.  Classic is
        a standalone installation on Windows or Linux where containerized is
        installed in a Linux Kubernetes or other Kubernetes cluster.  If installing
        in an AWS EC2 instance (for example) it would be 'classic'.  If installing
        in Google's GKE, it would be 'containerized'.  True = classic, False = containerized.
        (default is True).

    Attributes
    ----------
    session : requests.Session
        The underlying HTTP session used for all requests.
    data_flow : DataFlowManagement
        Access to probe management, ranges, and credentials.
    data_model : DataModel
        Access to the UCMDB class model and attributes.
    topology : Topology
        Access to CI and Relationship querying and creation.
    discovery : Discovery
        Access to discovery jobs and inventory tools.
    mgmt_zones : ManagementZones
        Access to management zone configurations.
    policies : Policies
        Access to policy and compliance features.
    integrations : Integrations
        Access to integration points and data push/pull jobs.
    reports : Reports
        Access to UCMDB reports and query results.
    system : System
        Access to server status, licensing, and general settings.
    settings : Settings
        Access to infrastructure settings.
    packages : Packages
        Access to Content Pack management.
    expose : ExposeCI
        Access to CI export/expose features.
    ldap : RetrieveLDAP
        Access to LDAP configuration.
    """
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
        self.version = (0,0,0)
        self._initialize_version()

    def _authenticate(self, user, password):
        """
        Authenticate with the UCMDB server and retrieves a token.

        This method sends a POST request to the /authenticate endpoint. 
        Upon success, it updates the session headers with the new token.

        Returns
        -------
        str
            The retrieved authentication token.

        Raises
        ------
        UCMDBAuthError
            If authentication fails due to invalid credentials or server 
            unreachability.
        """
        payload = {"username": user, "password": password, "clientContext": self.client_context}

        try:
            response = self.session.post(f"{self.base_url}/authenticate", json=payload)
            response.raise_for_status() # Good practice to check for 4xx/5xx errors
            
            token = response.json().get("token")
            self.session.headers.update({"Authorization": f"Bearer {token}"})
            return token
            
        except RequestException as e:
            raise UCMDBAuthError(f"Failed to connect to UCMDB at {self.base_url}: {e}")
    def _initialize_version(self):
        """
        Uses the system.getUCMDBVersion method to retrieve the version of this UCMDB server
        """
        try:
            server_ver = self.system.getUCMDBVersion().json()
            v_str = server_ver.get('fullServerVersion')
            self.version = tuple(map(int,v_str.split('.')))
        except Exception:
            self.version = (11,6,11)
