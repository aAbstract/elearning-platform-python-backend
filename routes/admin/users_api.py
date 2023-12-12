from fastapi import APIRouter, Header

from models.web.admin.users_requests import get_user_info_request, delete_user_request, delete_users_request, get_owned_lectures_request, update_user_request, lec_ownership_request

import lib.log as log_man
import routes.routes_utils as routes_utils
import lib.http_response as http_resp_man
import database.users_database_api as users_database_api
import database.users_lectures_database_api as users_lectures_database_api


# module config
_ROOT_ROUTE = f"{routes_utils.API_ROOT}/admin/users"
_MODULE_ID = 'routes.admin.users_api'
_ALLOWED_USERS = ['ADMIN']

# module state
router = APIRouter()


@router.post(f"{_ROOT_ROUTE}/get-user-info")
async def get_user_info(req: get_user_info_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.get_user_info"

    log_man.add_log(func_id, 'DEBUG',
                    f"received get user info admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    # fetch user full record
    db_api_resp = users_database_api.get_user_info(req.username)

    if len(db_api_resp.record) == 0:
        return http_resp_man.create_json_response(
            success=False,
            msg='User Not Found'
        )

    return http_resp_man.create_json_response(data={
        'user_record': db_api_resp.record[0]
    })


@router.post(f"{_ROOT_ROUTE}/rm-user")
async def delete_user(req: delete_user_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.delete_user"

    log_man.add_log(func_id, 'DEBUG',
                    f"received remove user admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = users_database_api.remove_user(req.username)

    return http_resp_man.create_json_response(
        msg=db_api_resp.msg,
        success=db_api_resp.success,
    )


@router.post(f"{_ROOT_ROUTE}/rm-lec-ownership")
async def delete_lec_ownership(req: lec_ownership_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.delete_lec_ownership"

    log_man.add_log(func_id, 'DEBUG',
                    f"received remove lecture ownership admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = users_lectures_database_api.delete_ownerships(
        req.user_id, req.lecture_id)

    return http_resp_man.create_json_response(
        msg=db_api_resp.msg,
        success=db_api_resp.success,
    )


@router.post(f"{_ROOT_ROUTE}/add-lec-ownership")
async def add_lec_ownership(req: lec_ownership_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.add_lec_ownership"

    log_man.add_log(func_id, 'DEBUG',
                    f"received add lecture ownership admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = users_lectures_database_api.add_ownership(
        req.user_id, req.lecture_id)

    return http_resp_man.create_json_response(
        msg=db_api_resp.msg,
        success=db_api_resp.success,
    )


@router.post(f"{_ROOT_ROUTE}/get-all-users")
async def get_all_users(authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.get_all_users"

    log_man.add_log(func_id, 'DEBUG', 'received get all users admin request')

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    # fetch all users from database
    db_api_resp = users_database_api.get_all_users()
    return http_resp_man.create_json_response(data=db_api_resp.record)


@router.post(f"{_ROOT_ROUTE}/delete-users")
async def delete_users(req: delete_users_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.delete_users"

    log_man.add_log(func_id, 'DEBUG',
                    f"received remove users list admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    # delete users from database
    db_api_resp = users_database_api.remove_users(req.username_list)

    return http_resp_man.create_json_response(
        msg=db_api_resp.msg,
        success=db_api_resp.success,
    )


@router.post(f"{_ROOT_ROUTE}/get-owned-lectures")
async def get_owned_lectures(req: get_owned_lectures_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.get_owned_lectures"

    log_man.add_log(func_id, 'DEBUG',
                    f"received get owned lectures admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = users_lectures_database_api.get_ownerships_data(req.user_id)

    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )

    return http_resp_man.create_json_response(
        data=db_api_resp.record,
    )


@router.post(f"{_ROOT_ROUTE}/update-user")
async def update_user(req: update_user_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.update_user"

    log_man.add_log(func_id, 'DEBUG',
                    f"received update user admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = users_database_api.update_user(req)

    return http_resp_man.create_json_response(
        success=db_api_resp.success,
        msg=db_api_resp.msg,
    )
