from models.internal.database_api import database_api_response

import database.database_driver as database_driver
import lib.log as log_man
import database.database_api_utils as database_api_utils


# module config
_MODULE_ID = 'database.users_lectures_database_api'


def get_ownerships(user_id: int) -> database_api_response:
    func_id = f"{_MODULE_ID}.get_ownerships"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT lecture_id
    FROM users_lectures
    WHERE user_id = %s;
    '''

    log_man.add_log(func_id,
                    'DEBUG', f"executing query {sql_query}, with values [{user_id}]")

    try:
        database_cursor.execute(sql_query, [user_id])

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(
            func_id, 'ERROR', err_msg)

        return database_api_response(success=False, msg=err_msg)

    res_record = database_api_utils.parse_sql_res(database_cursor)
    return database_api_response(record=res_record)


def get_ownerships_data(user_id: int) -> database_api_response:
    func_id = f"{_MODULE_ID}.get_ownerships_data"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT
    DISTINCT(l.lecture_id) AS lec_id,
    l.lecture_name_en AS lec_name_en,
    (
    SELECT COUNT(*) = 1 FROM lectures l2
    INNER JOIN users_lectures ul ON l2.lecture_id = ul.lecture_id
    WHERE ul.user_id = %s AND l.lecture_id = l2.lecture_id
    ) AS is_owned
    FROM lectures l;
    '''

    log_man.add_log(func_id,
                    'DEBUG', f"executing query {sql_query}, with values [{user_id}]")

    try:
        database_cursor.execute(sql_query, [user_id])

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(
            func_id, 'ERROR', err_msg)

        return database_api_response(success=False, msg=err_msg)

    res_record = database_api_utils.parse_sql_res(database_cursor)
    return database_api_response(record=res_record)


def add_ownership(user_id: int, lecture_id: int) -> database_api_response:
    func_id = f"{_MODULE_ID}.add_ownership"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    INSERT INTO users_lectures (user_id, lecture_id)
    VALUES (%s, %s);
    '''

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values [{user_id}, {lecture_id}]")

    try:
        database_cursor.execute(sql_query, [user_id, lecture_id])
        database_connection.commit()

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(
            func_id, 'ERROR', err_msg)

        return database_api_response(success=False, msg=err_msg)

    return database_api_response(msg='OK')


def delete_ownerships(user_id: int, lecture_id: int) -> database_api_response:
    func_id = f"{_MODULE_ID}.delete_ownerships"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    DELETE
    FROM users_lectures
    WHERE user_id = %s AND lecture_id = %s;
    '''

    log_man.add_log(func_id,
                    'DEBUG', f"executing query {sql_query}, with values [{user_id}, {lecture_id}]")

    try:
        database_cursor.execute(sql_query, [user_id, lecture_id])
        database_connection.commit()

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(
            func_id, 'ERROR', err_msg)

        return database_api_response(success=False, msg=err_msg)

    return database_api_response(msg='OK')
