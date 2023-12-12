from fastapi import APIRouter, Header

from models.web.admin.materials_requests import add_vid_doc_request, delete_materials_request, update_vid_doc_request, add_quiz_request, update_quiz_request

import lib.log as log_man
import routes.routes_utils as routes_utils
import lib.http_response as http_resp_man
import database.materials_database_api as materials_database_api


# module config
_ROOT_ROUTE = f"{routes_utils.API_ROOT}/admin/materials"
_MODULE_ID = 'routes.admin.materials_api'
_ALLOWED_USERS = ['ADMIN']

# module state
router = APIRouter()


@router.post(f"{_ROOT_ROUTE}/get-all-mats")
async def get_all_mats(authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.get_all_mats"

    log_man.add_log(func_id, 'DEBUG',
                    'received get all materials admin request')

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = materials_database_api.get_all_materials()

    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )

    return http_resp_man.create_json_response(
        data=db_api_resp.record,
    )


@router.post(f"{_ROOT_ROUTE}/add-vid-doc")
async def add_doc_vid(req: add_vid_doc_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.add_vid_doc"

    log_man.add_log(
        func_id, 'DEBUG', f"received add materials (video, document) admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = materials_database_api.add_vid_doc_mat(req)

    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )

    return http_resp_man.create_json_response(data={
        'mat_id': db_api_resp.record[0]['mat_id'],
    })


@router.post(f"{_ROOT_ROUTE}/add-quiz")
async def add_quiz(req: add_quiz_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.add_quiz"

    log_man.add_log(
        func_id, 'DEBUG', f"received add materials (quiz) admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = materials_database_api.add_quiz_mat(req)

    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )

    return http_resp_man.create_json_response(data={
        'mat_id': db_api_resp.record[0]['mat_id'],
    })


@router.post(f"{_ROOT_ROUTE}/update-vid-doc")
async def update_vid_doc(req: update_vid_doc_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.update_vid_doc"

    log_man.add_log(
        func_id, 'DEBUG', f"received upate material (video, document) admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = materials_database_api.update_vid_doc(req)

    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )

    db_api_resp = materials_database_api.get_mat_info(req.mat_id)

    if not db_api_resp.success:
        return http_resp_man.create_json_response(
            success=False,
            msg=db_api_resp.msg,
        )

    return http_resp_man.create_json_response(data={
        'material_record': db_api_resp.record[0],
    })


@router.post(f"{_ROOT_ROUTE}/delete-materials")
async def delete_material(req: delete_materials_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.delete_materials"

    log_man.add_log(
        func_id, 'DEBUG', f"received delete materials admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = materials_database_api.delete_materials(req)

    return http_resp_man.create_json_response(
        success=db_api_resp.success,
        msg=db_api_resp.msg,
    )


@router.post(f"{_ROOT_ROUTE}/update-quiz")
async def update_quiz(req: update_quiz_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.update_quiz"

    log_man.add_log(
        func_id, 'DEBUG', f"received update quiz admin request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp

    db_api_resp = materials_database_api.update_quiz(req)

    return http_resp_man.create_json_response(
        success=db_api_resp.success,
        msg=db_api_resp.msg,
    )
