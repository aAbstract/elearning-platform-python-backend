from fastapi import APIRouter, Header

import lib.log as log_man
import routes.routes_utils as routes_utils
import lib.http_response as http_resp_man
import database.lectures_database_api as lectures_database_api

from models.web.lectures_requests import get_lec_cont_request, get_quiz_answers_request


# module config
_ROOT_ROUTE = f"{routes_utils.API_ROOT}/lectures"
_MODULE_ID = 'routes.lectures_api'
_ALLOWED_USERS = ['STUDENT', 'ADMIN']

# module state
router = APIRouter()


@router.post(f"{_ROOT_ROUTE}/get-lectures")
async def get_lectures(authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.get_lectures"

    log_man.add_log(func_id, 'DEBUG', "received get lectures request")

    # authorize user
    user_id = -1
    auth_resp = routes_utils.authorize_api(
        authorization, ['STUDENT', 'ADMIN', 'NONE'], func_id)
    if auth_resp['success']:
        user_id = auth_resp['data']['token_obj']['user_id']

    # call lectures database API
    db_api_resp = lectures_database_api.get_lectures(user_id)

    if not db_api_resp.success:
        return http_resp_man.create_json_response(success=False, msg=db_api_resp.msg)

    return http_resp_man.create_json_response(data=db_api_resp.record)


@router.post(f"{_ROOT_ROUTE}/get-lecture-content")
async def get_lec_cont(req: get_lec_cont_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.get_lec_cont"

    log_man.add_log(func_id, 'DEBUG',
                    f"received get lecture content request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    # call lectures database API
    db_api_resp = lectures_database_api.get_lec_content(req.lec_id)

    if not db_api_resp.success:
        return http_resp_man.create_json_response(success=False, msg=db_api_resp.msg)

    return http_resp_man.create_json_response(data=db_api_resp.record)


@router.post(f"{_ROOT_ROUTE}/get-quiz-answers")
async def get_quiz_answers(req: get_quiz_answers_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.get_quiz_answers"

    log_man.add_log(func_id, 'DEBUG',
                    f"received get quiz answers request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    # call lectures database API
    db_api_resp = lectures_database_api.get_quiz_answers(req.quiz_id)

    if not db_api_resp.success:
        return http_resp_man.create_json_response(success=False, msg=db_api_resp.msg)

    return http_resp_man.create_json_response(data=db_api_resp.record)


@router.post(f"{_ROOT_ROUTE}/get-content-meta")
async def get_content_meta(req: get_lec_cont_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.get_content_meta"

    log_man.add_log(func_id, 'DEBUG',
                    f"received get lecture content meta data request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    # call lectures database API
    db_api_resp = lectures_database_api.get_lecture_content_meta_data(
        req.lec_id)

    if not db_api_resp.success:
        return http_resp_man.create_json_response(success=False, msg=db_api_resp.msg)

    return http_resp_man.create_json_response(data=db_api_resp.record)
