"""
This is the class that will be used to create an instance of a UCMDB Server.  Pass
the user/pass/UCMDB Server/Port and the base_url will be created and the authenticate
method will be created, then the headers with the token will be automatically updated
so the user only has to instanciate the UCMDBServer class and then call any methods
that will be used by it, keeping the authorization fresh and the headers pre-set
"""

import requests
from .dataflowmanagement import DataFlowManagement
from .datamodel import DataModel
from .policies import Policies
from .topology import Topology

class UCMDBAuthError(Exception):
    """
    This handles errors raised during UCMDB authentication
    """
    pass

class UCMDBServer:
    def __init__(self,user,password,server,port=8443,protocol='https',ssl_validation=False,client_context=1):
        self.base_url = f'{protocol}://{server}:{port}/rest-api'
        self.client_context = client_context
        self.session = requests.Session()
        self.session.verify = ssl_validation
        self.session.headers.update({
                'Content-Type':'application/json',
                'Accept':'application/json'
            })
        self._authenticate(user,password,client_context)
        self.dataflowmanagement = DataFlowManagement(self)
        self.datamodel = DataModel(self)
        self.policies = Policies(self)
        self.topology = Topology(self)
    
    
    def _authenticate(self, user,password,client_context):
        payload = {
        'username': user,
        'password': password,
        'clientContext': client_context
        }
        auth_url = f'{self.base_url}/authenticate'
        try:
            response = self.session.post(auth_url, json=payload)

            if response.status_code == 200:
                data = response.json()
                token_header = f"Bearer {data['token']}"
                self.session.headers.update({'Authorization':token_header})
            else:
                error_msg = (
                    f'Your user is not authorized.  Status: {response.status_code}\n'
                    f'Server Response: {response.text}'
                )

                raise UCMDBAuthError(error_msg)
        except UCMDBAuthError:
            raise 
        except Exception as e:
            raise ConnectionError(f'Could not connect to UCMDB at {self.base_url}.  Check to see that the server is running')
