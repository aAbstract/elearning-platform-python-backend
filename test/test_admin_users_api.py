import requests
import json
import random
import string
import jwt

import _test_config


def test_admin_users_api_lock():
    token_http_resp = _test_config.login_user('tuser', 'student_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/users/get-user-info"

    json_body = {
        'username': 'eslam',
    }

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, json=json_body, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert (json_obj['success'] == False and json_obj['msg']
            == 'Unauthorized API Access [Restricted Access]')


def test_admin_user_info_api():
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/users/get-user-info"

    json_body = {
        'username': 'eslam',
    }

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, json=json_body, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert json_obj['success']

    assert set(json_obj['data']['user_record'].keys()) == {'user_id', 'username', 'balance', 'user_role',
                                                           'phone_number', 'grade', 'center_name', 'parent_phone_number', 'full_name', 'pass_hash', 'email', 'reg_type'}


def test_admin_get_all_users_api():
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/users/get-all-users"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert json_obj['success']

    if len(json_obj['data']) != 0:
        assert set(json_obj['data'][0].keys()) == {'user_id', 'username', 'balance', 'user_role',
                                                   'phone_number', 'grade', 'center_name', 'parent_phone_number', 'full_name', 'pass_hash', 'email', 'reg_type'}


def test_admin_delete_users_api():
    # insert 5 users
    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/auth/signup"

    users_list = []

    for _ in range(5):
        random_sequence = ''.join(
            [random.choice(string.ascii_letters) for _ in range(8)])

        add_user_json = {
            'full_name': 'Eslam Elsharkawy',
            'username': f"test_user_{random_sequence}",
            'reg_type': 'ONLINE',
            'center_name': 'NONE',
            'grade': '0',
            'password': 'test_pass',
            'phone_number': '01012345678',
            'parent_phone_number': '01012345678',
            'email': 'test@test.com',
        }

        users_list.append(add_user_json)

        http_resp = requests.post(api_url, json=add_user_json)

        json_obj = json.loads(http_resp.content.decode())

        assert json_obj['success'] == True

        # decode jwt token
        token_obj = jwt.decode(json_obj['data']['access_token'],
                               'HfgtEYRkNJ58AOYJEYcLs0yChP5NfAdyfHMHYAmHtCBLT9tior1Y7lH7XPL99w20', algorithms=['HS512'])

        assert set(token_obj.keys()) == {
            'user_id', 'full_name', 'username', 'user_role', 'user_img', 'balance'}

    # delete 5 users
    # generate admin access token
    api_url = f"{server_url}/api/admin/users/delete-users"

    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')
    admin_access_token = token_http_resp['data']['access_token']

    username_list: list[str] = [user['username'] for user in users_list]

    headers = {
        'Authorization': f"Bearer {admin_access_token}",
    }

    json_body = {
        'username_list': username_list,
    }

    http_resp = requests.post(api_url, headers=headers, json=json_body)

    json_obj = json.loads(http_resp.content.decode())

    assert json_obj['success'] == True and json_obj['msg'] == 'OK'

    # check deletion routine
    api_url = f"{server_url}/api/admin/users/get-user-info"

    for useranme in username_list:
        json_body = {
            'username': useranme,
        }

        http_resp = requests.post(api_url, headers=headers, json=json_body)

        json_obj = json.loads(http_resp.content.decode())

        assert json_obj['success'] == False and json_obj['msg'] == 'User Not Found'


def test_admin_get_owned_lectures():
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/users/get-owned-lectures"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    json_body = {
        'user_id': 2,
    }

    http_resp = requests.post(api_url, headers=headers, json=json_body)

    json_obj = json.loads(http_resp.content.decode())

    assert json_obj['success']

    if len(json_obj['data']) != 0:
        assert set(json_obj['data'][0].keys()) == {'lec_id', 'lec_name_en', 'is_owned'}


def test_admin_update_user():
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/users/update-user"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    random_sequence = ''.join(
        [random.choice(string.ascii_letters) for _ in range(8)])

    json_body = {
        'full_name': f"Test User {random_sequence}",
        'username': 'tuser',
        'reg_type': 'OFFLINE',
        'center_name': 'NONE',
        'grade': 1,
        'password': 'student_pass_123',
        'is_password_changed': True,
        'phone_number': '01012345678',
        'parent_phone_number': '01012345678',
        'email': 'test@test.com',
        'user_role': 'STUDENT',
        'balance': 0.0,
    }

    http_resp = requests.post(api_url, headers=headers, json=json_body)

    json_obj = json.loads(http_resp.content.decode())

    assert json_obj['success'] and json_obj['msg'] == 'OK'

    api_url = f"{server_url}/api/admin/users/get-user-info"

    json_body = {
        'username': 'tuser',
    }

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, json=json_body, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert (json_obj['success'] and json_obj['data']['user_record']
            ['full_name'] == f"Test User {random_sequence}")

    json_body = {
        'full_name': 'Test User',
        'username': 'tuser',
        'reg_type': 'OFFLINE',
        'center_name': 'NONE',
        'grade': 1,
        'password': 'student_pass_123',
        'is_password_changed': True,
        'phone_number': '01012345678',
        'parent_phone_number': '01012345678',
        'email': 'test@test.com',
        'user_role': 'STUDENT',
        'balance': 0.0,
    }

    api_url = f"{server_url}/api/admin/users/update-user"

    http_resp = requests.post(api_url, headers=headers, json=json_body)

    json_obj = json.loads(http_resp.content.decode())

    assert json_obj['success'] and json_obj['msg'] == 'OK'

    api_url = f"{server_url}/api/admin/users/get-user-info"

    json_body = {
        'username': 'tuser',
    }

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, json=json_body, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert (json_obj['success'] and json_obj['data']
            ['user_record']['full_name'] == 'Test User')
