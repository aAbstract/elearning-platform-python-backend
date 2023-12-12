from models.internal.database_api import database_api_response
from models.web.admin.payment_logs_requests import delete_payment_logs_request

import lib.log as log_man
import database.database_driver as database_driver
import database.database_api_utils as database_api_utils


# modue config
_MODULE_ID = 'database.payments_database_api'


def add_payment_log(user_obj: dict, lecture_obj: dict) -> database_api_response:
    func_id = f"{_MODULE_ID}.make_payment"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    # add payment log
    sql_query = '''
    INSERT INTO payment_logs (user_id, log_datetime, payment_log_text)
    VALUES (%s, DATE_ADD(NOW(), interval 2 hour), %s);
    '''

    sql_vals = [
        user_obj['user_id'],
        f"User bought lecture: {lecture_obj['lecture_name_en']}, current balance: {user_obj['balance']}.",
    ]

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values {sql_vals}")

    try:
        database_cursor.execute(sql_query, sql_vals)

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(
            func_id, 'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    database_connection.commit()
    return database_api_response(msg='OK')


def add_recharge_log(coupon: str, user_obj: dict):
    func_id = f"{_MODULE_ID}.add_recharge_log"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    # add payment log
    sql_query = '''
    INSERT INTO payment_logs (user_id, log_datetime, payment_log_text)
    VALUES (%s, DATE_ADD(NOW(), interval 2 hour), %s);
    '''

    sql_vals = [
        user_obj['user_id'],
        f"User recharged coupon {coupon}, current balance: {user_obj['balance']}",
    ]

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values {sql_vals}")

    try:
        database_cursor.execute(sql_query, sql_vals)

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(
            func_id, 'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    database_connection.commit()
    return database_api_response(msg='OK')


def get_all_logs():
    func_id = f"{_MODULE_ID}.get_all_logs"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT
    pl.payment_log_id,
    pl.user_id,
    u.username,
    u.full_name,
    pl.log_datetime,
    pl.payment_log_text
    FROM payment_logs pl
    INNER JOIN users u
    ON pl.user_id = u.user_id;
    '''

    log_man.add_log(func_id, 'DEBUG', f"executing query {sql_query}")

    try:
        database_cursor.execute(sql_query)

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id, 'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    res_record = database_api_utils.parse_sql_res(database_cursor)
    return database_api_response(record=res_record)


def delete_logs(req: delete_payment_logs_request):
    func_id = f"{_MODULE_ID}.delete_logs"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    DELETE FROM payment_logs
    WHERE payment_log_id IN (%s);
    ''' % (','.join(['%s' for _ in range(len(req.payment_log_ids))]))

    log_man.add_log(
        func_id, 'DEBUG', f"executing query {sql_query}, with values {req.payment_log_ids}")

    try:
        database_cursor.execute(sql_query, req.payment_log_ids)
        database_connection.commit()

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id, 'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    return database_api_response(msg='OK')
