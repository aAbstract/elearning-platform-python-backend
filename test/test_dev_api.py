import requests
import json

import _test_config


def test_dev_update_database_connection():
    token_http_resp = _test_config.login_user('eslam_dev', 'student_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/dev/update-database-connection"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert json_obj['success'] and json_obj['msg'] == 'OK'
