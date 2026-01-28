import base64
import logging
import os

import urllib3
from ucmdb_rest import UCMDBServer

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
Use case:  This will display the reconciliation rule for any CIT specified.  Note that
this must be the 'name' attribute of the CI Type, not the 'Display Name'.
IPAddress = ip_address
Computer = host_node
"""

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("id_rule_decoder")

def main():
    script_dir = os.path.dirname(__file__)
    cred_path = os.path.join(script_dir,'credentials.json')
    client = UCMDBServer.from_json(cred_path)

    cit = input('Enter CI Type (e.g., node, ip_address): ') or "node"

    logger.info(f"Fetching class model for {cit}...")
    try:
        response = client.data_model.getClass(cit)
        
        if response.status_code == 200:
            my_output = response.json()
            
            try:
                encoded_xml = my_output["identification"]["ruleXml"]
                
                decoded_bytes = base64.b64decode(encoded_xml)
                decoded_xml_str = decoded_bytes.decode('utf-8')

                logger.info(f"\n--- Decoded Identification Rule for {cit} ---")
                print(decoded_xml_str)
                
            except (KeyError, TypeError):
                logger.warning(f"CI Type '{cit}' does not contain a 'ruleXml'.")
                logger.info("It likely inherits identification from its parent CI Type.")
        else:
            logger.error(f"Failed to fetch class. Status: {response.status_code}")

    except Exception as e:
        logger.critical(f"An error occurred: {e}")

if __name__ == "__main__":
    main()