import logging
import os

import urllib3
from ucmdb_rest import UCMDBServer

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
Use Case:  I want to look up specific attributes about a CI.  Most of the code in this section
is defining layout.  Required use of this libraray is in line 24 and line 42.  Yes, really, only
2 lines of code.  The rest is making nice layout or specifying examples.
"""

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("search_by_label_example")

def main():
    # 1. Load credentials and instanciate server object
    script_dir = os.path.dirname(__file__)
    cred_path = os.path.join(script_dir,'credentials.json')
    client = UCMDBServer.from_json(cred_path)

    # 2. Specify which attribute you would like. In this example we're using display_label and 
    #    node CI type, but this could be adapted to any CIT and any other attribute
    pattern = input('Enter label pattern (e.g., %Server%): ') or "%"
    cit = input('Enter CI Type (default: node): ') or "node"
    
    # Get the layout attributes
    my_layout = ["display_label", "name", "os_family", "serial_number", "global_id"]

    # 3. Search
    logger.info(f"Searching for {cit} matching '{pattern}'...")
    
    try:
        response = client.expose.search_by_label(
            label_pattern=pattern, 
            ci_type=cit, 
            layout=my_layout
        )
        
        if response.status_code == 200:
            results = response.json()
            
            if not results:
                logger.info("No matching CIs found.")
                return

            print(f"\nFound {len(results)} match(es):")
            print("-" * 105)
            print("|"+30*" "+"|"+15*" "+"|"+56*" "+"|")
            print("-" * 105)
            
            for ci in results:
                props = ci.get('properties', {})
                label = props.get('display_label', 'N/A')
                serial = props.get('serial_number', 'N/A')
                os_fam = props.get('os_family', 'N/A')
                
                print(f"| {label:<29}| {os_fam:<14}| {serial} |")
            print("-" * 105)

        else:
            logger.error(f"Error {response.status_code}: {response.text}")

    except Exception as e:
        logger.error(f"Search failed: {e}")

if __name__ == "__main__":
    main()