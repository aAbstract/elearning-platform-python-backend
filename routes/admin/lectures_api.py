from fastapi import APIRouter, Header, UploadFile

from models.web.admin.lectures_requests import add_lecture_request, delete_lectures_request, update_lecture_request

import lib.log as log_man
import routes.routes_utils as routes_utils
import database.lectures_database_api as lectures_database_api
import lib.http_response as http_resp_man


# module config
_ROOT_ROUTE = f"{routes_utils.API_ROOT}/admin/lectures"
_MODULE_ID = 'routes.admin.lectures_api'
_ALLOWED_USERS = ['ADMIN']

# module state
router = APIRouter()


@router.post(f"{_ROOT_ROUTE}/get-all-lecs")
async def get_all_lecs(authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.get_all_lecs"

    log_man.add_log(func_id, 'DEBUG',
                    'received get all lectures admin request')

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = lectures_database_api.get_all_lectures()

    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )

    return http_resp_man.create_json_response(
        data=db_api_resp.record,
    )


@router.post(f"{_ROOT_ROUTE}/add-lecture")
async def add_lecture(req: add_lecture_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.add_lecture"

    log_man.add_log(func_id, 'DEBUG',
                    f"received add lecture admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = lectures_database_api.add_lecture(req)

    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )

    return http_resp_man.create_json_response(
        data=db_api_resp.record[0],
    )


@router.post(f"{_ROOT_ROUTE}/delete-lecs")
async def delete_lecs(req: delete_lectures_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.delete_lecs"

    log_man.add_log(func_id, 'DEBUG',
                    f"received delete lectures admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = lectures_database_api.delete_lectures(req)

    return http_resp_man.create_json_response(
        success=db_api_resp.success,
        msg=db_api_resp.msg,
    )


@router.post(f"{_ROOT_ROUTE}/update-lecture")
async def update_lecture(req: update_lecture_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.update_lecture"

    log_man.add_log(func_id, 'DEBUG',
                    f"received update lecture admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = lectures_database_api.update_lecture(req)

    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )

    db_api_resp = lectures_database_api.get_lecture_info(req.lec_id)

    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )

    return http_resp_man.create_json_response(data={
        'lecture_record': db_api_resp.record[0],
    })


@router.post(f"{_ROOT_ROUTE}/get-lecs-data-source")
async def get_lecs_data_source(authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.get_lecs_data_source"

    log_man.add_log(func_id, 'DEBUG',
                    'received get lectures data source admin request')

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = lectures_database_api.get_lecs_data_source()

    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg
        )

    return http_resp_man.create_json_response(data=db_api_resp.record)


@router.post(f"{_ROOT_ROUTE}/upload-lec-thumbnail")
async def upload_lec_thumbnail(file: UploadFile, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.get_lecs_data_source"

    log_man.add_log(func_id, 'DEBUG',
                    'received get lectures data source admin request')

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    try:
        file_data = await file.read()
        with open(f"./public/thumbnails/{file.filename}", 'wb') as f:
            f.write(file_data)

    except Exception as err:
        return http_resp_man.create_json_response(success=False, msg=f"Error Saving File to Disk: {err}")

    return http_resp_man.create_json_response(
        msg=f"[File Uploaded] file_name: {file.filename}, file_size: {len(file_data)}"
    )
