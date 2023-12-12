import requests
import json

import _test_config


def test_get_lectures_api():
    server_url = _test_config.get_server_url()

    # login as a student
    token_http_resp = _test_config.login_user('eslam', 'student_pass_123')
    access_token = token_http_resp['data']['access_token']

    api_url = f"{server_url}/api/lectures/get-lectures"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    http_resp = requests.post(api_url, headers=headers)

    json_obj = json.loads(http_resp.content.decode())

    assert json_obj['success'] == True

    if len(json_obj['data']) != 0:
        assert set(json_obj['data'][0].keys()) == {'lec_id', 'lec_name_en', 'lec_name_ar',
                                                   'desc_en', 'desc_ar', 'thumbnail', 'vids_no', 'notes_no', 'quizes_no', 'is_owned', 'price', 'duration'}


def test_get_lecture_content():
    server_url = _test_config.get_server_url()

    # login as a student
    token_http_resp = _test_config.login_user('eslam', 'student_pass_123')
    access_token = token_http_resp['data']['access_token']

    api_url = f"{server_url}/api/lectures/get-lecture-content"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    json_body = {
        'lec_id': 1,
    }

    http_resp = requests.post(api_url, headers=headers, json=json_body)

    json_obj = json.loads(http_resp.content.decode())

    assert json_obj['success'] == True

    if len(json_obj['data']) != 0:
        assert set(json_obj['data'][0].keys()) == {
            'mat_id', 'mat_type', 'mat_order', 'name_en', 'name_ar', 'mat_link'}


def test_get_quiz_answers():
    server_url = _test_config.get_server_url()

    # login as a student
    token_http_resp = _test_config.login_user('eslam', 'student_pass_123')
    access_token = token_http_resp['data']['access_token']

    api_url = f"{server_url}/api/lectures/get-quiz-answers"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    json_body = {
        'quiz_id': 3,
    }

    http_resp = requests.post(api_url, headers=headers, json=json_body)

    json_obj = json.loads(http_resp.content.decode())

    assert json_obj['success'] == True

    if len(json_obj['data']) != 0:
        assert set(json_obj['data'][0].keys()) == {'question_order', 'answer'}


def test_get_lecture_content_meta():
    server_url = _test_config.get_server_url()

    # login as a student
    token_http_resp = _test_config.login_user('eslam', 'student_pass_123')
    access_token = token_http_resp['data']['access_token']

    api_url = f"{server_url}/api/lectures/get-content-meta"

    headers = {
        'Authorization': f"Bearer {access_token}",
    }

    json_body = {
        'lec_id': 1,
    }

    http_resp = requests.post(api_url, headers=headers, json=json_body)
    json_obj = json.loads(http_resp.content.decode())
    assert json_obj['success'] == True

    if len(json_obj['data']) != 0:
        assert set(json_obj['data'][0].keys()) == {
            'material_name_en', 'material_name_ar', 'material_type'}
