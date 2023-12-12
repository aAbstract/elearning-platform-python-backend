from fastapi import APIRouter

from models.web.auth_requests import login_request, signup_request

import routes.routes_utils as routes_utils
import lib.log as log_man
import lib.http_response as http_resp_man
import lib.crypto as cryp_man
import database.users_database_api as users_database_api
import lib.jwt as jwt_man


# module config
_ROOT_ROUTE = f"{routes_utils.API_ROOT}/auth"
_MODULE_ID = 'routes.auth_api'

# module state
router = APIRouter()


@router.post(f"{_ROOT_ROUTE}/login")
async def login_user(req: login_request):
    func_id = f"{_MODULE_ID}.login_user"

    log_man.add_log(func_id, 'DEBUG', f"received login request: {req}")

    # check if user in database
    password_hash = cryp_man.hash_password(req.password)
    user_record_api_response = users_database_api.get_user(
        req.username, password_hash)

    if not user_record_api_response.success:
        return http_resp_man.create_json_response(msg='Login faild, database query error', success=False)

    user_record = user_record_api_response.record

    if len(user_record) == 0:
        return http_resp_man.create_json_response(msg='Login faild, invalid username or password', success=False)

    # create jwt token
    user_obj = user_record[0]
    jwt_token = jwt_man.create_jwt_token({
        'user_id': user_obj['user_id'],
        'full_name': user_obj['full_name'],
        'username': user_obj['username'],
        'user_role': user_obj['user_role'],
        'user_img': 'img_avatar.png',
        'balance': user_obj['balance'],
    })

    # return http response object
    return http_resp_man.create_json_response(data={
        'access_token': jwt_token
    })


@router.post(f"{_ROOT_ROUTE}/signup")
async def signup_user(req: signup_request):
    func_id = f"{_MODULE_ID}.signup_user"

    log_man.add_log(func_id, 'DEBUG', f"received signup request: {req}")

    # check if user already exist in database
    database_username_api_response = users_database_api.get_username(
        req.username)

    if not database_username_api_response.success:
        return http_resp_man.create_json_response(msg='Signup faild, database query error', success=False)

    if len(database_username_api_response.record) != 0:
        return http_resp_man.create_json_response(msg='Username already exist', success=False)

    # insert user in database
    database_user_insert_api_response = users_database_api.add_user(req)

    if not database_user_insert_api_response.success:
        return http_resp_man.create_json_response(msg='Signup faild, database command error', success=False)

    # create jwt token
    jwt_token = jwt_man.create_jwt_token({
        'user_id': database_user_insert_api_response.record[0]['user_id'],
        'full_name': req.full_name,
        'username': req.username,
        'user_role': 'STUDENT',
        'user_img': 'img_avatar.png',
        'balance': 0,
    })

    # return http response object
    return http_resp_man.create_json_response(data={
        'access_token': jwt_token,
    })
