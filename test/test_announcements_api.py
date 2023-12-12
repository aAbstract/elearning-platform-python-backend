import requests
import json

import _test_config


def test_get_announcements_api():
    server_url = _test_config.get_server_url()

    # login as a student
    token_http_resp = _test_config.login_user('eslam', 'student_pass_123')
    access_token = token_http_resp['data']['access_token']

    api_url = f"{server_url}/api/announcements/get-announcements"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert json_obj['success'] == True
    if len(json_obj['data']) != 0:
        assert set(json_obj['data'][0].keys()) == {
            'announcement_desc_en', 'announcement_datetime', 'announcement_link', 'announcement_desc_ar', 'announcement_id'}
