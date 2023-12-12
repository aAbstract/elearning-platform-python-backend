import requests
import json
import jwt
import random
import string

import _test_config


def test_login_faild_api():
    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/auth/login"

    json_body = {
        'username': 'test_user',
        'password': 'test_pass',
    }

    http_resp = requests.post(api_url, json=json_body)

    json_obj = json.loads(http_resp.content.decode())

    assert (json_obj['success'] == False and json_obj['msg']
            == 'Login faild, invalid username or password')


def test_login_success_api():
    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/auth/login"

    json_body = {
        'username': 'eslam',
        'password': 'student_pass_123',
    }

    http_resp = requests.post(api_url, json=json_body)

    json_obj = json.loads(http_resp.content.decode())

    assert json_obj['success'] == True

    # decode jwt token
    token_obj = jwt.decode(json_obj['data']['access_token'],
                           'HfgtEYRkNJ58AOYJEYcLs0yChP5NfAdyfHMHYAmHtCBLT9tior1Y7lH7XPL99w20', algorithms=['HS512'])

    assert set(token_obj.keys()) == {
        'user_id', 'full_name', 'username', 'user_role', 'user_img', 'balance'}


def test_signup_user_exist_api():
    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/auth/signup"

    exist_user_json_obj = {
        'full_name': 'Eslam Elsharkawy',
        'username': 'eslam',
        'reg_type': 'ONLINE',
        'center_name': 'NONE',
        'grade': '0',
        'password': 'test_pass',
        'phone_number': '01012345678',
        'parent_phone_number': '01012345678',
        'email': 'test@test.com',
    }

    http_resp = requests.post(api_url, json=exist_user_json_obj)

    json_obj = json.loads(http_resp.content.decode())

    assert (json_obj['success'] == False and json_obj['msg']
            == 'Username already exist')


def test_signup_user_success_api():
    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/auth/signup"

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

    http_resp = requests.post(api_url, json=add_user_json)

    json_obj = json.loads(http_resp.content.decode())

    assert json_obj['success'] == True

    # decode jwt token
    token_obj = jwt.decode(json_obj['data']['access_token'],
                           'HfgtEYRkNJ58AOYJEYcLs0yChP5NfAdyfHMHYAmHtCBLT9tior1Y7lH7XPL99w20', algorithms=['HS512'])

    assert set(token_obj.keys()) == {
        'user_id', 'full_name', 'username', 'user_role', 'user_img', 'balance'}

    # test remove user api
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')
    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/users/rm-user"

    json_body = {
        'username': f"test_user_{random_sequence}",
    }

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, json=json_body, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert (json_obj['success'] and json_obj['msg'] == 'OK')
