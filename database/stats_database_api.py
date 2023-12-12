from models.internal.database_api import database_api_response

import database.database_driver as database_driver
import database.database_api_utils as database_api_utils
import lib.log as log_man

# module config
_MODULE_ID = 'database.stats_database_api'


def get_total_purchases() -> database_api_response:
    func_id = f"{_MODULE_ID}.get_total_purchases"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT
    SUM(l.price) AS total_purchases
    FROM users_lectures ul
    INNER JOIN lectures l
    ON ul.lecture_id = l.lecture_id;
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


def get_users_count_per_reg_type() -> database_api_response:
    func_id = f"{_MODULE_ID}.get_users_count_per_reg_type"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT
    u.reg_type,
    COUNT(u.user_id) AS users_count
    FROM users u
    GROUP BY u.reg_type;
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


def get_lecs_count() -> database_api_response:
    func_id = f"{_MODULE_ID}.get_lecs_count"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT COUNT(l.lecture_id) AS lecs_count FROM lectures l;
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


def get_mats_count_per_type() -> database_api_response:
    func_id = f"{_MODULE_ID}.get_mats_count_per_type"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT
    m.material_type,
    COUNT(m.material_id) AS materials_count
    FROM materials m
    GROUP BY m.material_type;
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


def get_users_count_per_center_name() -> database_api_response:
    func_id = f"{_MODULE_ID}.get_users_count_per_center_name"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT
    u.center_name,
    COUNT(u.user_id) AS users_count
    FROM users u
    GROUP BY u.center_name;
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


def get_lecs_ownership_counts() -> database_api_response:
    func_id = f"{_MODULE_ID}.get_lecs_ownership_counts"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT
    ownership_map.lecture_name_en,
    SUM(ownership_map.ownership_count) AS ownership_count
    FROM
    (
    SELECT
    l.lecture_id,
    l.lecture_name_en,
    ul.user_id,
    IF(ul.user_id IS NULL, 0, 1) AS ownership_count
    FROM lectures l
    LEFT OUTER JOIN users_lectures ul
    ON l.lecture_id = ul.lecture_id
    ) AS ownership_map
    GROUP BY ownership_map.lecture_id;
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
