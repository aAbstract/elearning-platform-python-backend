import requests
import json
import random
import string

import _test_config


def test_admin_lectures_api_lock():
    token_http_resp = _test_config.login_user('tuser', 'student_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/lectures/get-all-lecs"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert (json_obj['success'] == False and json_obj['msg']
            == 'Unauthorized API Access [Restricted Access]')


def test_admin_get_all_lectures_api():
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/lectures/get-all-lecs"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert json_obj['success']

    if len(json_obj['data']) != 0:
        assert set(json_obj['data'][0].keys()) == {'lecture_id', 'lecture_name_en', 'lecture_name_ar',
                                                   'lecture_desc_en', 'lecture_desc_ar', 'thumbnail', 'price', 'duration'}


def test_admin_add_lecture_api():
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/lectures/add-lecture"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    # add 5 random lectures
    lec_ids_list = []

    for _ in range(5):
        random_sequence = ''.join(
            [random.choice(string.ascii_letters) for _ in range(8)])

        add_lecture_json = {
            'lec_name_en': f"Test Lecture {random_sequence}",
            'lec_name_ar': 'محاضرة اختبار',
            'lec_desc_en': 'Test Desc',
            'lec_desc_ar': 'وصف اختبار',
            'thumbnail': 'th1.jpg',
            'duration': 5,
            'price': 200,
        }

        http_resp = requests.post(
            api_url, headers=headers, json=add_lecture_json)

        json_obj = json.loads(http_resp.content.decode())
        assert json_obj['success'] == True and ('lec_id' in json_obj['data'])
        lec_ids_list.append(json_obj['data']['lec_id'])

    # remove lectures
    api_url = f"{server_url}/api/admin/lectures/delete-lecs"

    json_body = {
        'lec_ids': lec_ids_list,
    }

    http_resp = requests.post(api_url, headers=headers, json=json_body)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success'] == True and json_obj['msg'] == 'OK'


def test_admin_update_lecture_api():
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/lectures/update-lecture"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    random_sequence = ''.join(
        [random.choice(string.ascii_letters) for _ in range(8)])

    json_body = {
        'lec_id': 1,
        'lec_name_en': f"Test Lecture {random_sequence}",
        'lec_name_ar': 'محاضرة اختبار',
        'lec_desc_en': 'Test Desc',
        'lec_desc_ar': 'وصف اختبار',
        'thumbnail': 'th1.jpg',
        'duration': 5,
        'price': 200,
    }

    http_resp = requests.post(api_url, headers=headers, json=json_body)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success'] and json_obj['data']['lecture_record'][
        'lecture_name_en'] == f"Test Lecture {random_sequence}"

    # revert changes
    json_body = {
        'lec_id': 1,
        'lec_name_en': 'Test Lecture One',
        'lec_name_ar': 'محاضرة اختبار',
        'lec_desc_en': 'Test Desc',
        'lec_desc_ar': 'وصف اختبار',
        'thumbnail': 'th1.jpg',
        'duration': 5,
        'price': 200,
    }

    http_resp = requests.post(api_url, headers=headers, json=json_body)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success'] and json_obj['data']['lecture_record'][
        'lecture_name_en'] == 'Test Lecture One'


def test_admin_get_lecs_data_source_api():
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/lectures/get-lecs-data-source"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert json_obj['success']

    if len(json_obj['data']) != 0:
        assert set(json_obj['data'][0].keys()) == {
            'lecture_id', 'lecture_name_en'}
