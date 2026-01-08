# -*- coding: utf-8 -*-
import pytest

# -*- coding: utf-8 -*-
import pytest

def test_recipient_email_modification_logic(ucmdb_client):
    """
    Simulates the old Command 95 logic: Fetch, modify local list, then PUT.
    """
    # 1. Setup - Ensure our test user exists
    test_name = "Logic_Test_User"
    setup_res = ucmdb_client.settings.addRecipients({
        'id': '', 
        'name': test_name, 
        'addresses': ['initial@test.com']
    })
    
    # Capture ID immediately for cleanup safety
    user_id = setup_res.json().get('id')

    try:
        # 2. Replicate Command 95 lookup
        response = ucmdb_client.settings.getRecipients()
        users = response.json()
        
        target_user = next((u for u in users if u['name'] == test_name), None)
        assert target_user is not None, f"User {test_name} not found after creation"
        
        # 3. Modify (Simulate 'a' for Add)
        target_user['addresses'].append('second@test.com')
        
        # 4. Push update
        update_res = ucmdb_client.settings.updateRecipients(user_id, target_user)
        assert update_res.status_code == 200
        
        # 5. Verify the change stuck
        final_list = ucmdb_client.settings.getRecipients().json()
        final_check = next(u for u in final_list if u['id'] == user_id)
        assert 'second@test.com' in final_check['addresses']
        
    finally:
        # Cleanup: Always runs even if assertions above fail
        if user_id:
            ucmdb_client.settings.deleteRecipients(user_id)

def test_setting_get_and_set_retention(ucmdb_client):
    """
    Tests getting a setting and setting it back to its original value.
    Setting: loggrabber.log.retention.period
    """
    target_setting = "loggrabber.log.retention.period"

    # 1. GET SETTING
    get_res = ucmdb_client.settings.getSetting(target_setting)
    assert get_res.status_code == 200
    
    setting_data = get_res.json()
    original_value = setting_data.get('value')
    assert original_value is not None
    
    # 2. SET SETTING (To the same value - "No-op" update)
    set_payload = {"value": original_value}
    set_res = ucmdb_client.settings.setSetting(target_setting, set_payload)
    
    assert set_res.status_code == 200
    assert set_res.json()['value'] == original_value