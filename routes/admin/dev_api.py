from fastapi import APIRouter, Header

import lib.log as log_man
import routes.routes_utils as routes_utils
import lib.http_response as http_resp_man
import database.dev_database_api as dev_database_api


# module config
_ROOT_ROUTE = f"{routes_utils.API_ROOT}/admin/dev"
_MODULE_ID = 'routes.admin.dev_api'
_ALLOWED_USERS = ['ADMIN']

# module state
router = APIRouter()


@router.post(f"{_ROOT_ROUTE}/update-database-connection")
async def update_database_connection(authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.update_database_connection"

    log_man.add_log(func_id, 'DEBUG',
                    'received update database connection admin request')

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    # delete users from database
    db_api_resp = dev_database_api.update_database_connection()

    return http_resp_man.create_json_response(
        msg=db_api_resp.msg,
        success=db_api_resp.success,
    )
