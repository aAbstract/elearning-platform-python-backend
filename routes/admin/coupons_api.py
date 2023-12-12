import random
import string
from fastapi import APIRouter, Header

from models.web.admin.coupons_requests import gen_coupon_list_request, delete_coupons_list_request

import lib.log as log_man
import routes.routes_utils as routes_utils
import lib.http_response as http_resp_man
import database.coupons_database_api as coupons_database_api


# module config
_ROOT_ROUTE = f"{routes_utils.API_ROOT}/admin/coupons"
_MODULE_ID = 'routes.admin.coupons_api'
_ALLOWED_USERS = ['ADMIN']

# module state
router = APIRouter()


@router.post(f"{_ROOT_ROUTE}/generate")
async def generate_coupons(req: gen_coupon_list_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.generate_coupons"

    log_man.add_log(func_id, 'DEBUG',
                    f"received generate coupons admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    # generate coupons list
    chars_list = string.ascii_uppercase + string.digits
    coupons_list = [
        ''.join([random.choice(chars_list) for _ in range(8)])
        for _ in range(req.coupons_list_count)
    ]

    # insert list in database
    database_api_resp = coupons_database_api.add_coupons_list(
        coupons_list, req.coupons_value)

    if not database_api_resp.success:
        return http_resp_man.create_json_response(success=False, msg=database_api_resp.msg)

    return http_resp_man.create_json_response(data={
        'coupons_list': coupons_list,
    })


@router.post(f"{_ROOT_ROUTE}/remove")
async def remove_coupons(req: delete_coupons_list_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.remove_coupons"

    log_man.add_log(func_id, 'DEBUG',
                    f"received remove coupons admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, ['STUDENT', 'ADMIN'], func_id)
    if not auth_resp['success']:
        return auth_resp

    # call remove coupons list database service
    database_api_resp = coupons_database_api.delete_coupon_list(req.coupons_list)

    if not database_api_resp.success:
        return http_resp_man.create_json_response(success=False, msg=database_api_resp.msg)

    return http_resp_man.create_json_response(msg='OK')


@router.post(f"{_ROOT_ROUTE}/get-all-coupons")
async def get_all_coupons(authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.get_all_coupons"

    log_man.add_log(func_id, 'DEBUG',
                    f"received get all coupons admin request")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = coupons_database_api.get_all_coupons()

    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )

    return http_resp_man.create_json_response(
        data=db_api_resp.record,
    )
