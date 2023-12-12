from fastapi import APIRouter, Header

from models.web.admin.payment_logs_requests import delete_payment_logs_request

import lib.log as log_man
import routes.routes_utils as routes_utils
import lib.http_response as http_resp_man
import database.payments_database_api as payments_database_api


# module config
_ROOT_ROUTE = f"{routes_utils.API_ROOT}/admin/payment-logs"
_MODULE_ID = 'routes.admin.payment_logs_api'
_ALLOWED_USERS = ['ADMIN']

# module state
router = APIRouter()


@router.post(f"{_ROOT_ROUTE}/get-all-logs")
async def get_all_logs(authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.get_all_logs"

    log_man.add_log(func_id, 'DEBUG',
                    'received get all payment logs admin request')

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = payments_database_api.get_all_logs()

    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )

    return http_resp_man.create_json_response(
        data=db_api_resp.record,
    )


@router.post(f"{_ROOT_ROUTE}/delete-logs")
async def delete_logs(req: delete_payment_logs_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.delete_logs"

    log_man.add_log(
        func_id, 'DEBUG', f"received delete payment logs admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = payments_database_api.delete_logs(req)

    return http_resp_man.create_json_response(
        success=db_api_resp.success,
        msg=db_api_resp.msg,
    )
