import pytest

def test_get_information_raw(ucmdb_client):
    """Verify raw payload submission to exposeCI."""
    payload = {
        "type": "ip_address",
        "layout": ["display_label"],
        "includeSubtypes": "false",
        "filtering": {
            "logicalOperator": "and",
            "conditions": []
        }
    }
    response = ucmdb_client.expose.getInformation(payload)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_search_nodes_helper(ucmdb_client):
    """Verify the search_nodes_by_label helper method."""
    # Using a wildcard that should return at least one result in most labs
    response = ucmdb_client.expose.search_nodes_by_label("%")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    if len(data) > 0:
        properties = data[0].get("properties", {})
        assert "display_label" in properties