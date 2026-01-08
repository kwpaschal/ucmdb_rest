# -*- coding: utf-8 -*-
import pytest

def test_package_metadata_queries(ucmdb_client):
    """
    Tests only the read-only GET methods for packages.
    """
    # 1. Test getPackages (List all)
    all_res = ucmdb_client.packages.getPackages()
    assert all_res.status_code == 200
    packages_list = all_res.json()
    assert len(packages_list) > 0, "No packages found on server"
    
    # Pick a real package from the list to use for specific tests
    sample_pkg = packages_list[0]
    pkg_zip_name = sample_pkg['name']        # e.g., 'A10_vthunder.zip'
    pkg_display_name = sample_pkg['displayName'] # e.g., 'A10_vthunder'

    # 2. Test getPackage (Specific metadata)
    single_res = ucmdb_client.packages.getPackage(pkg_zip_name)
    assert single_res.status_code == 200
    assert single_res.json()['name'] == pkg_zip_name

    # 3. Test filterPackage (UI Search endpoint)
    filter_res = ucmdb_client.packages.filterPackage(pkg_display_name)
    assert filter_res.status_code == 200
    # filterPackage returns {'collection': [...]}
    assert any(p['displayName'] == pkg_display_name for p in filter_res.json().get('collection', []))

    # 4. Test getProgress (Status check)
    progress_res = ucmdb_client.packages.getProgress(pkg_zip_name)
    assert progress_res.status_code == 200
    assert "status" in progress_res.json()

def test_content_pack_queries(ucmdb_client):
    """
    Tests read-only queries for Content Packs.
    """
    # 1. Get all Content Packs
    cp_res = ucmdb_client.packages.getContentPacks()
    assert cp_res.status_code == 200
    cp_list = cp_res.json()
    
    if cp_list:
        # 2. Get details for the first CP in the list
        first_cp_version = cp_list[0]['version']
        specific_res = ucmdb_client.packages.getSpecificContentPack(first_cp_version)
        assert specific_res.status_code == 200
        assert specific_res.json()['version'] == first_cp_version