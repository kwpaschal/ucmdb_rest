import logging
import os

import urllib3
from ucmdb_rest import UCMDBAuthError, UCMDBServer

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
Use case:  I need to get the version information from UCMDB?
"""

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Get Version")

def main():
    try:
        script_dir = os.path.dirname(__file__)
        cred_path = os.path.join(script_dir,'credentials.json')
        client = UCMDBServer.from_json(cred_path)
       
        logger.info(f"Connected to UCMDB Version: {client.server_version}")

        try:
            version = client.system.getUCMDBVersion()
            version_data = version.json()
            print(f'Product: {version_data["productName"]}')
            print(f'Server Version: {version_data["fullServerVersion"]}')
            print(f'Content Pack: {version_data["contentPackVersion"]}')
            print(f'Server Build: {version_data["serverBuildNumber"]}')
            print(f'My server version from the client: {client.server_version}')
            print(version_data)

        except Exception as e:
            logger.critical(f"An unexpected error occurred: {e}", exc_info=True)

    except UCMDBAuthError as e:
        logger.error(f"Authentication failed: {e}")

if __name__ == "__main__":
    main()
