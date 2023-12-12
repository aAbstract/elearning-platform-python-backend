from models.internal.database_api import database_api_response
from models.web.auth_requests import signup_request
from models.web.admin.users_requests import update_user_request

import database.database_driver as database_driver
import lib.log as log_man
import database.database_api_utils as database_api_utils
import lib.crypto as cryp_man


# module config
_MODULE_ID = 'database.users_database_api'


def get_user(username: str, password_hash: str) -> database_api_response:
    func_id = f"{_MODULE_ID}.get_user"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT *
    FROM users
    WHERE username = %s AND pass_hash = %s;
    '''

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values [{username}, {password_hash}]")

    try:
        database_cursor.execute(sql_query, [username, password_hash])
    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id,
                        'ERROR', err_msg)

        return database_api_response(success=False, msg=err_msg)

    res_record = database_api_utils.parse_sql_res(database_cursor)
    return database_api_response(record=res_record)


def get_username(username: str) -> database_api_response:
    func_id = f"{_MODULE_ID}.get_username"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT username
    FROM users
    WHERE username = %s;
    '''

    log_man.add_log(func_id,
                    'DEBUG', f"executing query {sql_query}, with values [{username}]")

    try:
        database_cursor.execute(sql_query, [username])
    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(
            func_id, 'ERROR', err_msg)

        return database_api_response(success=False, msg=err_msg)

    res_record = database_api_utils.parse_sql_res(database_cursor)
    return database_api_response(record=res_record)


def add_user(sig_req: signup_request) -> database_api_response:
    func_id = f"{_MODULE_ID}.add_user"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    INSERT INTO users (full_name, username, reg_type, center_name, grade, pass_hash, user_role, phone_number, parent_phone_number, email, balance)
    VALUES (%s, %s, %s, %s, %s, %s, 'STUDENT', %s, %s, %s, 0);
    '''

    password_hash = cryp_man.hash_password(sig_req.password)

    sql_vals = [
        sig_req.full_name,
        sig_req.username,
        sig_req.reg_type,
        sig_req.center_name,
        sig_req.grade,
        password_hash,
        sig_req.phone_number,
        sig_req.parent_phone_number,
        sig_req.email,
    ]

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values {sql_vals}")

    try:
        database_cursor.execute(sql_query, sql_vals)
        database_connection.commit()
    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id,
                        'ERROR', err_msg)

        return database_api_response(success=False, msg=err_msg)

    return database_api_response(record=[{
        'user_id': database_cursor.lastrowid
    }])


def get_user_info(username: str) -> database_api_response:
    func_id = f"{_MODULE_ID}.get_user_info"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT *
    FROM users
    WHERE username = %s;
    '''

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values [{username}]")

    try:
        database_cursor.execute(sql_query, [username])

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(
            func_id, 'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    res_record = database_api_utils.parse_sql_res(database_cursor)
    return database_api_response(record=res_record)


def update_user_balance(username: str, new_balance: float) -> database_api_response:
    func_id = f"{_MODULE_ID}.update_user_balance"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    UPDATE
    users
    SET
    balance = %s
    WHERE username = %s;
    '''

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values [{new_balance}, {username}]")

    try:
        database_cursor.execute(sql_query, [new_balance, username])
        database_connection.commit()

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(
            func_id, 'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    return database_api_response(msg='OK')


def recharge_coupon(user_id: int, coupon: str) -> database_api_response:
    func_id = f"{_MODULE_ID}.recharge_coupon"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    # load coupon value
    sql_query = '''
    SELECT coupon_value
    FROM coupons
    WHERE coupon_text = %s;
    '''

    log_man.add_log(func_id,
                    'DEBUG', f"executing query {sql_query}, with values [{coupon}]")

    try:
        database_cursor.execute(sql_query, [coupon])

    except Exception as err:
        err_msg = f"database error: {err}"

        log_man.add_log(
            func_id, 'ERROR', err_msg)

        return database_api_response(success=False, msg=err_msg)

    res_record = database_api_utils.parse_sql_res(database_cursor)

    if len(res_record) == 0:
        return database_api_response(success=False, msg='Invalid Coupon')

    coupon_val: float = res_record[0]['coupon_value']

    # update user balance
    sql_query = '''
    UPDATE
    users
    SET
    balance = balance + %s
    WHERE user_id = %s;
    '''

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values [{user_id}, {coupon_val}]")

    try:
        database_cursor.execute(sql_query, [coupon_val, user_id])
        database_connection.commit()

    except Exception as err:
        err_msg = f"database error: {err}"

        log_man.add_log(
            func_id, 'ERROR', err_msg)

        return database_api_response(success=False, msg=err_msg)

    # remove charged coupon from database
    sql_query = '''
    DELETE
    FROM coupons
    WHERE coupon_text = %s;
    '''

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values [{coupon}]")

    try:
        database_cursor.execute(sql_query, [coupon])
        database_connection.commit()

    except Exception as err:
        err_msg = f"database error: {err}"

        log_man.add_log(
            func_id, 'ERROR', err_msg)

        return database_api_response(success=False, msg=err_msg)

    return database_api_response(msg='OK')


def remove_user(username: str) -> database_api_response:
    func_id = f"{_MODULE_ID}.remove_user"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    DELETE
    FROM users
    WHERE username = %s;
    '''

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values [{username}]")

    try:
        database_cursor.execute(sql_query, [username])
        database_connection.commit()

    except Exception as err:
        err_msg = f"database error: {err}"

        log_man.add_log(func_id, 'ERROR', err_msg)

        return database_api_response(success=False, msg=err_msg)

    return database_api_response(msg='OK')


def get_all_users() -> database_api_response:
    func_id = f"{_MODULE_ID}.get_all_users"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT *
    FROM users;
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


def remove_users(username_list: list[str]) -> database_api_response:
    func_id = f"{_MODULE_ID}.remove_users"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    DELETE
    FROM users
    WHERE username IN (%s);
    ''' % (','.join(['%s' for _ in range(len(username_list))]))

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values {username_list}")

    try:
        database_cursor.execute(sql_query, username_list)
        database_connection.commit()

    except Exception as err:
        err_msg = f"database error: {err}"

        log_man.add_log(func_id, 'ERROR', err_msg)

        return database_api_response(success=False, msg=err_msg)

    return database_api_response(msg='OK')


def update_user(req: update_user_request) -> database_api_response:
    func_id = f"{_MODULE_ID}.update_user"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    UPDATE users
    SET
    full_name = %s,
    reg_type = %s,
    center_name = %s,
    grade = %s,
    pass_hash = %s,
    phone_number = %s,
    parent_phone_number = %s,
    email = %s,
    user_role = %s,
    balance = %s
    WHERE
    username = %s;
    '''

    password_hash = req.password
    if req.is_password_changed:
        password_hash = cryp_man.hash_password(req.password)

    sql_vals = [
        req.full_name,
        req.reg_type,
        req.center_name,
        req.grade,
        password_hash,
        req.phone_number,
        req.parent_phone_number,
        req.email,
        req.user_role,
        req.balance,
        req.username,
    ]

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values {sql_vals}")

    try:
        database_cursor.execute(sql_query, sql_vals)
        database_connection.commit()

    except Exception as err:
        err_msg = f"database error: {err}"

        log_man.add_log(func_id, 'ERROR', err_msg)

        return database_api_response(success=False, msg=err_msg)

    return database_api_response(msg='OK')
