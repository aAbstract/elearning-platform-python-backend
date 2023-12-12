from fastapi import APIRouter, Header

from models.web.admin.announcements_requests import add_announcement_request, delete_announcement_request

import lib.log as log_man
import routes.routes_utils as routes_utils
import lib.http_response as http_resp_man
import database.announcements_database_api as announcements_database_api


# module config
_ROOT_ROUTE = f"{routes_utils.API_ROOT}/admin/announcements"
_MODULE_ID = 'routes.admin.announcements_api'
_ALLOWED_USERS = ['ADMIN']

# module state
router = APIRouter()


@router.post(f"{_ROOT_ROUTE}/add-announcement")
async def add_announcement(req: add_announcement_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.add_announcement"

    log_man.add_log(func_id, 'DEBUG',
                    f"received add announcement admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = announcements_database_api.add_auuounce(req)

    if not db_api_resp.success:
        return http_resp_man.create_json_response(success=False, msg=db_api_resp.msg)

    return http_resp_man.create_json_response(
        data=db_api_resp.record[0]
    )


@router.post(f"{_ROOT_ROUTE}/delete-announcements")
async def delete_announcements(req: delete_announcement_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.delete_announcements"

    log_man.add_log(func_id, 'DEBUG',
                    f"received delete announcements admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = announcements_database_api.delete_auuounce(req)

    return http_resp_man.create_json_response(
        success=db_api_resp.success,
        msg=db_api_resp.msg,
    )
