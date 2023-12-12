import lib.http_response as http_resp_man
import lib.log as log_man
import lib.jwt as jwt_man


API_ROOT = '/api'


def authorize_api(auth_header: str, allowed_roles: list[str], func_id: str) -> dict:
    if auth_header == None:
        err_msg = 'Unauthorized API Access [Empty Authorization Header]'
        if 'NONE' not in allowed_roles:
            log_man.add_log(func_id, 'ERROR', err_msg)
        return http_resp_man.create_json_response(success=False, msg=err_msg)

    # validate authorization header
    token_obj = None
    try:
        access_token = auth_header.split(' ')[1]
        token_obj = jwt_man.decode_jwt_token(access_token)

    except:
        err_msg = 'Unauthorized API Access [Invalid Token]'
        if 'NONE' not in allowed_roles:
            log_man.add_log(func_id, 'ERROR', err_msg)
        return http_resp_man.create_json_response(success=False, msg=err_msg)

    # check logged in user
    if token_obj['user_role'] not in allowed_roles:
        err_msg = 'Unauthorized API Access [Restricted Access]'
        log_man.add_log(func_id, 'ERROR', err_msg)
        return http_resp_man.create_json_response(success=False, msg=err_msg)

    return http_resp_man.create_json_response(data={
        'token_obj': token_obj,
    })
