import requests
import json

import _test_config


def test_admin_stats_api_lock():
    token_http_resp = _test_config.login_user('tuser', 'student_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/stats/get-stats"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert (json_obj['success'] == False and json_obj['msg']
            == 'Unauthorized API Access [Restricted Access]')


def test_admin_get_stats_api():
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/stats/get-stats"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, headers=headers)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success']

    # validate total purchases
    assert 'total_purchases' in set(json_obj['data'].keys())

    # validate users count per registration type
    assert 'users_count_per_reg_type' in set(json_obj['data'].keys())
    if len(json_obj['data']['users_count_per_reg_type']) != 0:
        assert set(json_obj['data']['users_count_per_reg_type'][0].keys()) == {
            'reg_type', 'users_count'}

    # validate lectures count
    assert 'lecs_count' in set(json_obj['data'].keys())

    # validate materials count per type
    assert 'mats_count_per_mat_type' in set(json_obj['data'].keys())
    if len(json_obj['data']['mats_count_per_mat_type']) != 0:
        assert set(json_obj['data']['mats_count_per_mat_type'][0].keys()) == {
            'material_type', 'materials_count'}

    # validate users count per center names
    assert 'users_count_per_center_name' in set(json_obj['data'].keys())
    if len(json_obj['data']['users_count_per_center_name']) != 0:
        assert set(json_obj['data']['users_count_per_center_name'][0].keys()) == {
            'center_name', 'users_count'}

    # validate lectures ownership counts
    assert 'lecs_ownership_counts' in set(json_obj['data'].keys())
    if len(json_obj['data']['lecs_ownership_counts']) != 0:
        assert set(json_obj['data']['lecs_ownership_counts'][0].keys()) == {
            'lecture_name_en', 'ownership_count'}
