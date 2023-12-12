from fastapi import APIRouter, Header

from models.web.payment_requests import make_payment_request
from models.web.payment_requests import recharge_balance_request

import lib.log as log_man
import routes.routes_utils as routes_utils
import lib.http_response as http_resp_man
import database.payments_database_api as payments_database_api
import database.users_database_api as users_database_api
import database.users_lectures_database_api as users_lectures_database_api
import database.lectures_database_api as lectures_database_api


# module config
_ROOT_ROUTE = f"{routes_utils.API_ROOT}/payments"
_MODULE_ID = 'routes.payments_api'
_ALLOWED_USERS = ['ADMIN', 'STUDENT']

# module state
router = APIRouter()


@router.post(f"{_ROOT_ROUTE}/make-payment")
async def make_payment(req: make_payment_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.make_payment"

    log_man.add_log(func_id, 'DEBUG',
                    f"received make payment request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp
    token_obj = auth_resp['data']['token_obj']

    # check if lecture is already owned
    user_id: int = token_obj['user_id']
    lecture_id: int = req.lecture_id

    user_ownerships = users_lectures_database_api.get_ownerships(user_id)

    if lecture_id in [x['lecture_id'] for x in user_ownerships.record]:
        return http_resp_man.create_json_response(success=False, msg='Payment Request Faild, Lecture Already Owned')

    # check balance
    username: str = token_obj['username']

    user_obj = users_database_api.get_user_info(username).record[0]
    lecture_obj = lectures_database_api.get_lecture_info(lecture_id).record[0]

    if user_obj['balance'] < lecture_obj['price']:
        return http_resp_man.create_json_response(success=False, msg='Payment Request Faild, Not Enough Balance')

    # withdraw payment
    new_balance: float = user_obj['balance'] - lecture_obj['price']
    withdraw_db_resp = users_database_api.update_user_balance(
        username, new_balance)

    if not withdraw_db_resp.success:
        return http_resp_man.create_json_response(success=False, msg='Payment Request Faild, Balance Withdraw Error')

    # add lecture ownership
    add_ownership_db_resp = users_lectures_database_api.add_ownership(
        user_id, lecture_id)

    if not add_ownership_db_resp.success:
        return http_resp_man.create_json_response(success=False, msg=add_ownership_db_resp.msg)

    db_api_resp = users_database_api.get_user_info(token_obj['username'])

    if not db_api_resp.success:
        return http_resp_man.create_json_response(success=False, msg=db_api_resp.msg)

    new_user_obj = db_api_resp.record[0]

    # add payment log
    add_payment_log_db_resp = payments_database_api.add_payment_log(
        new_user_obj, lecture_obj)

    if not add_payment_log_db_resp.success:
        return http_resp_man.create_json_response(success=False, msg=add_payment_log_db_resp.msg)

    return http_resp_man.create_json_response(data={
        'balance': new_user_obj['balance']
    })


@router.post(f"{_ROOT_ROUTE}/recharge-balance")
async def recharge_balance(req: recharge_balance_request, authorization=Header(default=None)):
    func_id = f"{_MODULE_ID}.recharge_balance"

    log_man.add_log(func_id, 'DEBUG',
                    f"received recharge balance request: {req}")

    # authorize user
    auth_resp = routes_utils.authorize_api(
        authorization, _ALLOWED_USERS, func_id)
    if not auth_resp['success']:
        return auth_resp
    token_obj = auth_resp['data']['token_obj']

    # call recharge balance database API
    db_api_resp = users_database_api.recharge_coupon(
        token_obj['user_id'], req.coupon)
    if not db_api_resp.success:
        return http_resp_man.create_json_response(success=False, msg=db_api_resp.msg)

    # return new balance
    user_obj = users_database_api.get_user_info(
        token_obj['username']).record[0]

    # add payment log
    add_payment_log_db_resp = payments_database_api.add_recharge_log(
        req.coupon, user_obj)

    if not add_payment_log_db_resp.success:
        return http_resp_man.create_json_response(success=False, msg=add_payment_log_db_resp.msg)

    return http_resp_man.create_json_response(data={
        'new_balance': user_obj['balance'],
    })
