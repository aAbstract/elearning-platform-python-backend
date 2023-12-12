from fastapi import APIRouter

import lib.log as log_man
import routes.routes_utils as routes_utils
import lib.http_response as http_resp_man
import database.announcements_database_api as announcements_database_api


# module config
_ROOT_ROUTE = f"{routes_utils.API_ROOT}/announcements"
_MODULE_ID = 'routes.announcements_api'

# module state
router = APIRouter()


@router.post(f"{_ROOT_ROUTE}/get-announcements")
async def get_announcements():
    func_id = f"{_MODULE_ID}.get_announcements"

    log_man.add_log(func_id, 'DEBUG', 'received get announcements request')

    db_api_resp = announcements_database_api.get_announces()

    if not db_api_resp.success:
        return http_resp_man.create_json_response(success=False, msg=db_api_resp.msg)

    return http_resp_man.create_json_response(data=db_api_resp.record)
