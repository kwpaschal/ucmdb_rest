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
logger = logging.getLogger("run view example")

def main():
    # 2. INITIALIZE CLIENT
    try:
        script_dir = os.path.dirname(__file__)
        cred_path = os.path.join(script_dir,'credentials.json')
        client = UCMDBServer.from_json(cred_path)
       
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
