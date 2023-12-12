import requests
import json

import _test_config


def test_admin_payment_logs_api_lock():
    token_http_resp = _test_config.login_user('tuser', 'student_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/payment-logs/get-all-logs"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert (json_obj['success'] == False and json_obj['msg']
            == 'Unauthorized API Access [Restricted Access]')


def test_admin_get_all_logs_api():
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/payment-logs/get-all-logs"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert json_obj['success']

    if len(json_obj['data']) != 0:
        assert set(json_obj['data'][0].keys()) == {
            'payment_log_id', 'user_id', 'username', 'full_name', 'log_datetime', 'payment_log_text'}
