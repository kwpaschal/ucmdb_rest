import logging

from ucmdb_rest import UCMDBAuthError, UCMDBServer

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
        
        client = UCMDBServer(
            user="admin", 
            password="password123", 
            server="ucmdb-server.example.com"
        )
        logger.info(f"Connected to UCMDB Version: {client.server_version}")

        # 3. PREPARE DATA
        ci_to_add = {"cis": [
                        {
                            "ucmdbId": "temporary_id_1",
                            "type": "unix",
                            "properties": {
                                "display_label": "MyLinuxServer",
                                "name": "MyLinuxServer"
                            }
                        },
                        {
                            "ucmdbId": "temporary_id_2",
                            "type": "running_software",
                            "properties": {
                                "discovered_product_name": "My Custom Software"
                            }
                        }
                    ],
            "relations": [
                        {
                            "ucmdbId": "temp_rel_1",
                            "type": "composition",
                            "end1Id": "temporary_id_1",
                            "end2Id": "temporary_id_2",
                            "properties": {}
                        }
                    ]
            }
        # 4. EXECUTE AND LOG RESULTS
        logger.info("Attempting to add new Node CI...")
        result = client.topology.add_cis(ci_to_add)
        
        # We log the resulting ID returned by the library
        logger.info(f"Successfully added CI. UCMDB ID: {result}")

    except UCMDBAuthError as e:
        logger.error(f"Authentication failed: {e}")
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
