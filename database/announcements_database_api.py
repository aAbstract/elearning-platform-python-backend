from models.internal.database_api import database_api_response
from models.web.admin.announcements_requests import add_announcement_request, delete_announcement_request

import database.database_driver as database_driver
import lib.log as log_man
import database.database_api_utils as database_api_utils


# module config
_MODULE_ID = 'database.announcements_database_api'


def get_announces() -> database_api_response:
    func_id = f"{_MODULE_ID}.get_announces"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT *
    FROM announcements;
    '''

    log_man.add_log(func_id, 'DEBUG', f"executing query {sql_query}")

    try:
        database_cursor.execute(sql_query)

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id,
                        'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    res_record = database_api_utils.parse_sql_res(database_cursor)
    return database_api_response(record=res_record)


def add_auuounce(req: add_announcement_request) -> database_api_response:
    func_id = f"{_MODULE_ID}.add_auuounce"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    INSERT INTO announcements (announcement_desc_en, announcement_desc_ar, announcement_link, announcement_datetime)
    VALUES (%s, %s, %s, %s);
    '''

    sql_vals = [
        req.announcement_desc_en,
        req.announcement_desc_ar,
        req.announcement_link,
        req.announcement_datetime,
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
        'announcement_id': database_cursor.lastrowid,
    }])


def delete_auuounce(req: delete_announcement_request) -> database_api_response:
    func_id = f"{_MODULE_ID}.delete_auuounce"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    DELETE FROM announcements
    WHERE announcement_id IN (%s);
    ''' % (','.join(['%s' for _ in range(len(req.announcement_ids))]))

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values {req.announcement_ids}")

    try:
        database_cursor.execute(sql_query, req.announcement_ids)
        database_connection.commit()

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id,
                        'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    return database_api_response(msg='OK')
