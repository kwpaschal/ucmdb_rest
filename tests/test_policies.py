# -*- coding: utf-8 -*-
import pytest
from ucmdb_rest.policies import ComplianceStatus


def test_policies_full_lifecycle(ucmdb_client):
    """
    Tests the complete compliance workflow:
    1. Get available views
    2. Get specific view definition
    3. Calculate the view to get an execution ID
    4. Retrieve all non-compliant CIs using the auto-chunker
    """
    
    views_res = ucmdb_client.policies.getComplainceViews()
    assert views_res.status_code == 200
    views = views_res.json()
    assert len(views) > 0, "No compliance views found in UCMDB"
    
    target_view_name = views[0]['name']
    
    view_detail_res = ucmdb_client.policies.getSpecificComplianceView(target_view_name)
    assert view_detail_res.status_code == 200
    view_definition = view_detail_res.json()
    
    calc_res = ucmdb_client.policies.calculateComplianceView(view_definition)
    assert calc_res.status_code == 200
    
    execution_data = calc_res.json()
    execution_id = execution_data.get('viewResultId')
    assert execution_id is not None, "Failed to get viewResultId from calculation"
    
    non_compliant_results = ucmdb_client.policies.getAllResultsForPath(
        execution_id, 
        status_type=ComplianceStatus.NON_COMPLIANT
    )
    
    assert isinstance(non_compliant_results, list)
    
    print(f"\n--- Policy Audit: {target_view_name} ---")
    print(f"Total Non-Compliant Items Found: {len(non_compliant_results)}")
    
    if len(non_compliant_results) > 0:
        sample_ci = non_compliant_results[0].get('ci')
        assert sample_ci is not None
        assert 'id' in sample_ci
        print(f"Sample Breached CI ID: {sample_ci['id']}")
        print(f"Breached Policies: {non_compliant_results[0].get('breachedPolicies')}")

def test_get_policies_list(ucmdb_client):
    """Simple test to verify policy listing works."""
    response = ucmdb_client.policies.getPolicies()
    assert response.status_code == 200
    policies = response.json()
    assert isinstance(policies, list)
    if len(policies) > 0:
        assert 'name' in policies[0]

def test_calculateView(ucmdb_client):
    result = ucmdb_client.policies.calculateView("All My Windows Servers")
    assert result.status_code == 200