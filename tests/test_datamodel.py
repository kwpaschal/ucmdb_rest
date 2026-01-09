import pytest

myCI = {
           "cis": [
                {
                   "ucmdbId": "1",
                   "type": "node",
                   "properties": {"name":"Test6",
                                  "os_family":"windows"}
                }
            ],
            "relations": []
        }

ci_list = []
node_global_id = None

def test_addCIs(ucmdb_client):
    global ci_list, node_global_id
    # Use returnIdsMap=True to get the mapping of temp IDs to real IDs
    result = ucmdb_client.data_model.addCIs(myCI, returnIdsMap=True)
    
    assert result.status_code == 200
    data = result.json()
    print(data)
    
    if "idsMap" in data:
        ci_list = list(data["idsMap"].values())
        node_global_id = data["idsMap"].get("1")
    else:
        ci_list = data.get("addedCis", []) + data.get("ignoredCis", [])
        if ci_list:
            node_global_id = ci_list[0]

    assert len(ci_list) > 0
    assert node_global_id is not None

def test_updateCI(ucmdb_client):
    global node_global_id
    updatedCI = {"ucmdbId":node_global_id,
                 "type":"node",
                 "properties" : {"data_note":"Updated by REST"}}
    response = ucmdb_client.data_model.updateCI(node_global_id, updatedCI)
    
    assert response.status_code == 200
    data = response.json()
    assert node_global_id in data.get("updatedCis", []) or node_global_id in data.get("ignoredCis", [])

def test_deleteCIs(ucmdb_client):
    global ci_list
    for ci_id in ci_list:
        response = ucmdb_client.data_model.deleteCIs(ci_id, isGlobalId=True)
        assert response.status_code == 200

def test_getClass(ucmdb_client):
    response = ucmdb_client.data_model.getClass("node")
    assert response.status_code == 200

def test_retrieveIdentificationRule(ucmdb_client):
    response = ucmdb_client.data_model.retrieveIdentificationRule("node")
    assert response.status_code == 200

def test_convertFromBase64_logic(ucmdb_client):
    sample_input = "SGVsbG8gVUNNREI="
    expected_output = "Hello UCMDB"

    result = ucmdb_client.data_model.convertFromBase64(sample_input)
    assert result == expected_output