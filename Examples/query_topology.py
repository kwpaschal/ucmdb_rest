import json
import logging
import os

import urllib3
from ucmdb_rest import UCMDBAuthError, UCMDBServer

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
Use case:  How can I pull a list of CIs from a specific UCMDB TQL?
"""

# 1. SETUP LOGGING
# We configure the root logger to show both our messages and the library's messages
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("add_cis_example")

def main():
    # 2. INITIALIZE CLIENT
    try:
        # If you want to see deep details (like raw URLs), uncomment the next line:
        # logging.getLogger("ucmdb_rest").setLevel(logging.DEBUG)
        # Load credentials from credentials.json in the same path
        cred_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
        with open(cred_path, 'r') as f:
            creds = json.load(f)


        client = UCMDBServer(
            user=creds['user'],
            password=creds['password'],
            server=creds['server'],
            port=creds.get('port', 8443),
            ssl_validation=creds.get('ssl_validation', False)
        )
       
        logger.info(f"Connected to UCMDB Version: {client.server_version}")

        view_name = "All My Windows Servers"
        logger.info(f'**Running View: {view_name}')

        topology = client.topology.runView(view_name)
        cis = topology.json().get('cis',[])
        logger.info(f'Found {len(cis)} CIs in view')
        logger.info('Printing out the top 5 CIs')

        for ci in cis[:5]:
            props = ci.get('properties',{})
            logger.info(f' - {props.get('display_label')} ({ci.get('type')})')

    except UCMDBAuthError as e:
        logger.error(f"Authentication failed: {e}")
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
