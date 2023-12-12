import requests
import json

import _test_config


def test_admin_coupons_api_lock():
    token_http_resp = _test_config.login_user('tuser', 'student_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/coupons/generate"

    json_body = {
        'coupons_list_count': 5,
        'coupons_value': 150,
    }

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, json=json_body, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert (json_obj['success'] == False and json_obj['msg']
            == 'Unauthorized API Access [Restricted Access]')


def test_admin_coupons_api():
    # add coupons list
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/coupons/generate"

    list_count = 5

    json_body = {
        'coupons_list_count': list_count,
        'coupons_value': 150,
    }

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, json=json_body, headers=headers)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success']
    assert len(json_obj['data']['coupons_list']) == list_count

    # test validation stage 1
    generated_coupons_list = json_obj['data']['coupons_list']
    api_url = f"{server_url}/api/admin/coupons/get-all-coupons"
    http_resp = requests.post(api_url, headers=headers)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success']
    assert len(json_obj['data']) == list_count

    api_url = f"{server_url}/api/admin/coupons/remove"

    json_body = {
        'coupons_list': generated_coupons_list,
    }

    http_resp = requests.post(api_url, json=json_body, headers=headers)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success'] == True

    # test validation stage 2
    api_url = f"{server_url}/api/admin/coupons/get-all-coupons"
    http_resp = requests.post(api_url, headers=headers)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success']
    assert len(json_obj['data']) == 0
