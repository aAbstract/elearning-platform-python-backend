import requests
import json
import random
import string

import _test_config


def test_admin_materials_api_lock():
    token_http_resp = _test_config.login_user('tuser', 'student_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/materials/get-all-mats"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert (json_obj['success'] == False and json_obj['msg']
            == 'Unauthorized API Access [Restricted Access]')


def test_admin_get_all_materials_api():
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/materials/get-all-mats"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert json_obj['success']

    if len(json_obj['data']) != 0:
        assert set(json_obj['data'][0].keys()) == {'material_name_ar', 'material_id', 'lecture_id',
                                                   'lecture_name_en', 'material_link', 'material_name_en', 'material_order', 'material_type'}


def test_admin_add_mat_vid_doc_api():
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/materials/add-vid-doc"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    # add video
    add_vid_json = {
        'linked_lec_id': 2,
        'mat_type': 'VIDEO',
        'mat_order': 1,
        'mat_name_en': 'Test Video One',
        'mat_name_ar': 'فيديو اختبار واحد',
        'mat_link': 'https://www.youtube.com/embed/_qCYbJUZwJ8',
    }

    http_resp = requests.post(api_url, headers=headers, json=add_vid_json)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success'] == True and ('mat_id' in json_obj['data'])
    vid_id = json_obj['data']['mat_id']

    # add document
    add_doc_json = {
        'linked_lec_id': 2,
        'mat_type': 'DOCUMENT',
        'mat_order': 2,
        'mat_name_en': 'Test Document One',
        'mat_name_ar': 'ملف اختبار واحد',
        'mat_link': 'https://drive.google.com/file/d/1pApQFcAr2_XaiJ0mNRx1SzKHtfxoW2rO/preview',
    }

    http_resp = requests.post(api_url, headers=headers, json=add_doc_json)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success'] == True and ('mat_id' in json_obj['data'])
    doc_id = json_obj['data']['mat_id']

    # remove materials
    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/materials/delete-materials"

    json_body = {
        'items': [
            {
                'is_quiz': False,
                'mat_id': vid_id,
            },
            {
                'is_quiz': False,
                'mat_id': doc_id,
            },
        ],
    }

    http_resp = requests.post(api_url, headers=headers, json=json_body)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success'] == True and json_obj['msg'] == 'OK'


def test_admin_update_mat_vid_doc_api():
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/materials/update-vid-doc"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    random_sequence = ''.join(
        [random.choice(string.ascii_letters) for _ in range(8)])

    json_body = {
        'mat_id': 1,
        'linked_lec_id': 2,
        'mat_type': 'VIDEO',
        'mat_order': 1,
        'mat_name_en': f"Test Video {random_sequence}",
        'mat_name_ar': 'فيديو اختبار واحد',
        'mat_link': 'https://www.youtube.com/embed/_qCYbJUZwJ8',
    }

    http_resp = requests.post(api_url, headers=headers, json=json_body)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success'] == True
    assert json_obj['data']['material_record'][
        'material_name_en'] == f"Test Video {random_sequence}"

    # revert changes
    json_body = {
        'mat_id': 1,
        'linked_lec_id': 1,
        'mat_type': 'VIDEO',
        'mat_order': 1,
        'mat_name_en': 'Test Video One',
        'mat_name_ar': 'فيديو اختبار واحد',
        'mat_link': 'https://www.youtube.com/embed/_qCYbJUZwJ8',
    }

    http_resp = requests.post(api_url, headers=headers, json=json_body)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success'] == True
    assert json_obj['data']['material_record'][
        'material_name_en'] == 'Test Video One'


def test_admin_add_mat_quiz_api():
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/materials/add-quiz"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    # add video
    add_quiz_json = {
        'linked_lec_id': 2,
        'mat_type': 'QUIZ',
        'mat_order': 1,
        'mat_name_en': 'Test Quiz One',
        'mat_name_ar': 'اختبار واحد',
        'mat_link': 'https://drive.google.com/file/d/1pApQFcAr2_XaiJ0mNRx1SzKHtfxoW2rO/preview',
        'quiz_answers': [
            {
                'question_order': 1,
                'question_answer': 'A',
            },
            {
                'question_order': 2,
                'question_answer': 'B',
            },
            {
                'question_order': 3,
                'question_answer': 'C',
            },
        ],
    }

    http_resp = requests.post(api_url, headers=headers, json=add_quiz_json)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success'] == True and ('mat_id' in json_obj['data'])
    quiz_id = json_obj['data']['mat_id']

    # remove quiz
    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/materials/delete-materials"

    json_body = {
        'items': [
            {
                'is_quiz': True,
                'mat_id': quiz_id,
            },
        ],
    }

    http_resp = requests.post(api_url, headers=headers, json=json_body)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success'] == True and json_obj['msg'] == 'OK'


def test_admin_upate_mat_quiz_api():
    token_http_resp = _test_config.login_user('ahesham', 'admin_pass_123')

    access_token = token_http_resp['data']['access_token']

    server_url = _test_config.get_server_url()
    api_url = f"{server_url}/api/admin/materials/update-quiz"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    json_body = {
        'mat_id': 3,
        'linked_lec_id': 1,
        'mat_type': 'QUIZ',
        'mat_order': 3,
        'mat_name_en': 'Test Quiz One',
        'mat_name_ar': 'اختبار اختباري واحد',
        'mat_link': 'https://drive.google.com/file/d/1jVG_2Sf2tBa8HODwBhYJAjr3KxSeu2ls/preview',
        'quiz_answers': [
            {
                'question_order': 1,
                'question_answer': 'X',
            },
            {
                'question_order': 2,
                'question_answer': 'B',
            },
            {
                'question_order': 3,
                'question_answer': 'A',
            },
            {
                'question_order': 4,
                'question_answer': 'D',
            },
            {
                'question_order': 5,
                'question_answer': 'D',
            },
            {
                'question_order': 6,
                'question_answer': 'B',
            },
            {
                'question_order': 7,
                'question_answer': 'C',
            },
            {
                'question_order': 8,
                'question_answer': 'B',
            },
            {
                'question_order': 9,
                'question_answer': 'B',
            },
            {
                'question_order': 10,
                'question_answer': 'C',
            },
        ],
    }

    http_resp = requests.post(api_url, headers=headers, json=json_body)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success'] == True and json_obj['msg'] == 'OK'

    # revert changes
    json_body['quiz_answers'][0]['question_answer'] = 'B'
    http_resp = requests.post(api_url, headers=headers, json=json_body)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success'] == True and json_obj['msg'] == 'OK'
