import requests
import json
import jwt

import _test_config


def test_payment_routine():
    server_url = _test_config.get_server_url()

    # login as a student
    token_http_resp = _test_config.login_user('eslam', 'student_pass_123')
    access_token = token_http_resp['data']['access_token']

    # check if lecture is owned
    api_url = f"{server_url}/api/payments/make-payment"

    json_body = {
        'lecture_id': 1,
    }

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, json=json_body, headers=headers)
    json_obj = json.loads(http_resp.content.decode())
    assert (json_obj['success'] == False and json_obj['msg']
            == 'Payment Request Faild, Lecture Already Owned')

    # login as admin
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')
    admin_access_token = token_http_resp['data']['access_token']

    # generate coupon
    api_url = f"{server_url}/api/admin/coupons/generate"

    json_body = {
        'coupons_list_count': 1,
        'coupons_value': 200,
    }

    headers = {
        'Authorization': f"Bearer {admin_access_token}",
    }

    http_resp = requests.post(api_url, json=json_body, headers=headers)
    json_obj = json.loads(http_resp.content.decode())
    coupon: str = json_obj['data']['coupons_list'][0]
    assert len(coupon) != 0

    # login as tuser
    token_http_resp = _test_config.login_user('tuser', 'student_pass_123')
    access_token = token_http_resp['data']['access_token']

    # use fake coupon and check
    api_url = f"{server_url}/api/payments/recharge-balance"

    json_body = {
        'coupon': 'fake_coupon',
    }

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, json=json_body, headers=headers)
    json_obj = json.loads(http_resp.content.decode())
    assert (json_obj['success'] == False and json_obj['msg']
            == 'Invalid Coupon')

    # use coupon to recharge balance and check
    api_url = f"{server_url}/api/payments/recharge-balance"

    json_body = {
        'coupon': coupon,
    }

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, json=json_body, headers=headers)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['data']['new_balance'] >= 200

    # make purchase and check
    old_balance: float = json_obj['data']['new_balance']

    api_url = f"{server_url}/api/payments/make-payment"

    json_body = {
        'lecture_id': 1,
    }

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, json=json_body, headers=headers)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['data']['balance'] == old_balance - 200

    # delete lecture ownership
    api_url = f"{server_url}/api/admin/users/rm-lec-ownership"

    user_id = jwt.decode(access_token, options={
                         "verify_signature": False})['user_id']

    json_body = {
        'user_id': user_id,
        'lecture_id': 1,
    }

    headers = {
        'Authorization': f"Bearer {admin_access_token}",
    }

    http_resp = requests.post(api_url, json=json_body, headers=headers)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['msg'] == 'OK'
