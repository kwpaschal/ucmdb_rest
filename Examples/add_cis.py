import ucmdb_rest

#creates a session with a UCMDB server.  Parameters are Username, Password,
# UCMDB Server, Port (optional), Protocol (http or https) (optional),
# verify SSL certificate (True or False) Client context (client number)
# and Classic or Containerized (classic=true, containerized=false)
client = ucmdb_rest.UCMDBServer('user', 'pass', 'myucmdb.mycompany.com', 
                                    port=8443, 
                                    protocol='https', 
                                    verify=False, 
                                    client_id=1, 
                                    is_classic=True)
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
response = client.data_model.addCIs(ci_to_add)

if response.status_code == 200:
    print('Sucessfully added CIs')
    print(response.json())
else:
    print(f'Failed to add CIs: {response.text}')