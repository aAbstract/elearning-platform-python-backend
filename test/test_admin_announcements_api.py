import requests
import json

import _test_config


def test_admin_announcements_api_lock():
    token_http_resp = _test_config.login_user('tuser', 'student_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/announcements/add-announcement"

    json_body = {
        'announcement_desc_en': 'Test Announcement',
        'announcement_desc_ar': 'Test Announcement',
        'announcement_link': 'NONE',
        'announcement_datetime': '2023-3-1',
    }

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, json=json_body, headers=headers)
    json_obj = json.loads(http_resp.content.decode())
    assert (json_obj['success'] == False and json_obj['msg']
            == 'Unauthorized API Access [Restricted Access]')


def test_admin_announcements_api():
    # add coupons list
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/announcements/add-announcement"

    json_body = {
        'announcement_desc_en': 'Test Announcement',
        'announcement_desc_ar': 'Test Announcement',
        'announcement_link': 'NONE',
        'announcement_datetime': '2023-3-1',
    }

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, json=json_body, headers=headers)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success']
    assert 'announcement_id' in json_obj['data'].keys()

    announcement_id = json_obj['data']['announcement_id']
    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/announcements/delete-announcements"

    json_body = {
        'announcement_ids': [announcement_id],
    }

    http_resp = requests.post(api_url, json=json_body, headers=headers)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success'] and json_obj['msg'] == 'OK'
