from fastapi import APIRouter, Header

import lib.log as log_man
import routes.routes_utils as routes_utils
import database.users_database_api as users_database_api
import lib.http_response as http_resp_man


# module config
_ROOT_ROUTE = f"{routes_utils.API_ROOT}/user"
_MODULE_ID = 'routes.user_api'
_ALLOWED_USERS = ['ADMIN', 'STUDENT']

# module state
router = APIRouter()


@router.post(f"{_ROOT_ROUTE}/get-balance")
async def get_balance(authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.get_balance"

    log_man.add_log(func_id, 'DEBUG', 'received get user balance request')

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp
    token_obj = auth_resp['data']['token_obj']

    username: int = token_obj['username']
    db_api_resp = users_database_api.get_user_info(username)

    if not db_api_resp.success:
        return http_resp_man.create_json_response(success=False, msg=db_api_resp.msg)

    return http_resp_man.create_json_response(
        data={
            'balance': db_api_resp.record[0]['balance'],
        },
    )
