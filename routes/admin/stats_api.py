from fastapi import APIRouter, Header

import lib.log as log_man
import routes.routes_utils as routes_utils
import database.stats_database_api as stats_database_api
import lib.http_response as http_resp_man


# module config
_ROOT_ROUTE = f"{routes_utils.API_ROOT}/admin/stats"
_MODULE_ID = 'routes.admin.stats'
_ALLOWED_USERS = ['ADMIN']

# module state
router = APIRouter()


@router.post(f"{_ROOT_ROUTE}/get-stats")
async def get_stats(authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.get_stats"

    log_man.add_log(func_id, 'DEBUG', 'received get stats admin request')

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    # compute total purchases
    db_api_resp = stats_database_api.get_total_purchases()
    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )
    total_purchases = db_api_resp.record[0]['total_purchases']

    # compute users count per registration type
    db_api_resp = stats_database_api.get_users_count_per_reg_type()
    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )
    users_count_per_reg_type = db_api_resp.record

    # compute lectures count
    db_api_resp = stats_database_api.get_lecs_count()
    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )
    lecs_count = db_api_resp.record[0]['lecs_count']

    # compute materials count per material type
    db_api_resp = stats_database_api.get_mats_count_per_type()
    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )
    mats_count_per_mat_type = db_api_resp.record

    # compute users count per center name
    db_api_resp = stats_database_api.get_users_count_per_center_name()
    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )
    users_count_per_center_name = db_api_resp.record

    # compute lectures ownership counts
    db_api_resp = stats_database_api.get_lecs_ownership_counts()
    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )
    lecs_ownership_counts = db_api_resp.record

    return http_resp_man.create_json_response(data={
        'total_purchases': total_purchases,
        'users_count_per_reg_type': users_count_per_reg_type,
        'lecs_count': lecs_count,
        'mats_count_per_mat_type': mats_count_per_mat_type,
        'users_count_per_center_name': users_count_per_center_name,
        'lecs_ownership_counts': lecs_ownership_counts,
    })
