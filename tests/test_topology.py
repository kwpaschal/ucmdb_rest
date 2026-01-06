import pytest

test_query = {
                    "nodes": [
                        {
                            "type": "node",
                            "queryIdentifier": "node",
                            "visible": "true",
                            "includeSubtypes": "true",
                            "layout": ["display_label"],
                            "attributeConditions": [],
                            "linkConditions": [],
                            "ids": []
                        }
                    ],
                    "relations": []
                }

def test_queryCIs(ucmdb_client):
    result = ucmdb_client.topology.queryCIs(test_query)
    assert result.status_code == 200

def test_view_with_forced_chunking(ucmdb_client):
    results = ucmdb_client.topology.get_all_view_results("All My Windows Servers", chunkSize=2)
    assert len(results['cis']) > 0

def test_view_default_behavior(ucmdb_client):
    results = ucmdb_client.topology.get_all_view_results("All My Windows Servers")
    assert len(results['cis']) > 0