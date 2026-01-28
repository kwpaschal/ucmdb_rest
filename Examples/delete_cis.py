import logging
import os

import urllib3
from ucmdb_rest import UCMDBAuthError, UCMDBServer

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
Use case:  How can I delete one or more CIs from UCMDB?
"""

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Delete CI example")

def main():
    try:
        script_dir = os.path.dirname(__file__)
        cred_path = os.path.join(script_dir,'credentials.json')
        client = UCMDBServer.from_json(cred_path)
       
        logger.info(f"Connected to UCMDB Version: {client.server_version}")

        id_to_delete = input('Enter the UCMDB ID to remove: ')
        logger.info(f'Attempting to delete id: {id_to_delete}')
        try:
            response = client.data_model.deleteCIs(id_to_delete)

            if response.status_code == 200:
                logger.info(f'Successfully deleted {id_to_delete}')
            else:
                logger.error(f'Failed to delete.  Status: {response.status_code}')
                logger.error(f'Response: {response.text}')
        except Exception as e:
            logger.critical(f"An unexpected error occurred: {e}", exc_info=True)

    except UCMDBAuthError as e:
        logger.error(f"Authentication failed: {e}")

if __name__ == "__main__":
    main()
