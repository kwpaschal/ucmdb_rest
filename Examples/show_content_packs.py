import logging
import os

import urllib3
from ucmdb_rest import UCMDBServer

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
Use Case:  Show the installed content packs.
"""

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("content_pack_explorer")

def main():
    script_dir = os.path.dirname(__file__)
    cred_path = os.path.join(script_dir,'credentials.json')
    client = UCMDBServer.from_json(cred_path)
    logger.info(f"Connected to {client.server}. Fetching Content Pack information...\n")

    try:
        response = client.packages.getContentPacks()
        
        if response.status_code == 200:
            content_packs = response.json()
            
            if isinstance(content_packs, list) and len(content_packs) > 0:
                print(f"\n{'Attribute':<25} | {'Value'}")
                print("-" * 50)
                
                # We iterate through the first (or only) item in the list
                info = content_packs[0]
                for key, value in info.items():
                    # Only show fields that actually have data
                    if value is not None and value != '':
                        print(f"{key:<25} | {value}")
        else:
            logger.error(f"Failed to fetch content packs. Status: {response.status_code}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()