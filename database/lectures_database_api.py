from models.internal.database_api import database_api_response
from models.web.admin.lectures_requests import add_lecture_request, delete_lectures_request, update_lecture_request

import database.database_driver as database_driver
import database.database_api_utils as database_api_utils
import lib.log as log_man

# module config
_MODULE_ID = 'database.lectures_database_api'


def get_lecture_info(lecture_id: int) -> database_api_response:
    func_id = f"{_MODULE_ID}.get_lecture_info"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT *
    FROM lectures
    WHERE lecture_id = %s;
    '''

    log_man.add_log(func_id,
                    'DEBUG', f"executing query {sql_query}, with values [{lecture_id}]")

    try:
        database_cursor.execute(sql_query, [lecture_id])

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id, 'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    res_record = database_api_utils.parse_sql_res(database_cursor)
    return database_api_response(record=res_record)


def get_lectures(user_id: int) -> database_api_response:
    func_id = f"{_MODULE_ID}.get_lectures"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT
    DISTINCT(l.lecture_id) AS lec_id,
    l.lecture_name_en AS lec_name_en,
    l.lecture_name_ar AS lec_name_ar,
    l.lecture_desc_en AS desc_en,
    l.lecture_desc_ar AS desc_ar,
    l.thumbnail,
    l.price,
    l.duration,
    (
    SELECT COUNT(*) FROM lectures l
    INNER JOIN materials m ON l.lecture_id = m.lecture_id
    WHERE m.material_type  = 'VIDEO'
    ) AS vids_no,
    (
    SELECT COUNT(*) FROM lectures l
    INNER JOIN materials m ON l.lecture_id = m.lecture_id
    WHERE m.material_type  = 'DOCUMENT'
    ) AS notes_no,
    (
    SELECT COUNT(*) FROM lectures l
    INNER JOIN materials m ON l.lecture_id = m.lecture_id
    WHERE m.material_type  = 'QUIZ'
    ) AS quizes_no,
    (
    SELECT COUNT(*) = 1 FROM lectures l2
    INNER JOIN users_lectures ul ON l2.lecture_id = ul.lecture_id
    WHERE ul.user_id = %s AND l.lecture_id = l2.lecture_id
    ) AS is_owned
    FROM lectures l
    LEFT OUTER JOIN materials m ON l.lecture_id = m.lecture_id;
    '''

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values [{user_id}]")

    try:
        database_cursor.execute(sql_query, [user_id])

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id, 'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    res_record = database_api_utils.parse_sql_res(database_cursor)

    return database_api_response(record=res_record)


def get_lec_content(lec_id: int) -> database_api_response:
    func_id = f"{_MODULE_ID}.get_lec_content"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT
    m.material_id AS mat_id,
    m.material_type AS mat_type,
    m.material_order AS mat_order,
    m.material_name_en AS name_en,
    m.material_name_ar AS name_ar,
    m.material_link AS mat_link
    FROM lectures l
    INNER JOIN materials m ON l.lecture_id = m.lecture_id
    WHERE l.lecture_id = %s
    ORDER BY m.material_order ASC;
    '''

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values [{lec_id}]")

    try:
        database_cursor.execute(sql_query, [lec_id])

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id, 'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    res_record = database_api_utils.parse_sql_res(database_cursor)

    return database_api_response(record=res_record)


def get_quiz_answers(quiz_id: int) -> database_api_response:
    func_id = f"{_MODULE_ID}.get_quiz_answers"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT
    qa.question_order AS question_order,
    qa.answer_char AS answer
    FROM materials m
    INNER JOIN quiz_answers qa ON m.material_id = qa.material_id
    WHERE qa.material_id = %s
    ORDER BY qa.question_order ASC;
    '''

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values [{quiz_id}]")

    try:
        database_cursor.execute(sql_query, [quiz_id])

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id, 'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    res_record = database_api_utils.parse_sql_res(database_cursor)

    return database_api_response(record=res_record)


def get_all_lectures() -> database_api_response:
    func_id = f"{_MODULE_ID}.get_all_lectures"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = 'SELECT * FROM lectures l;'

    log_man.add_log(func_id, 'DEBUG', f"executing query {sql_query}")

    try:
        database_cursor.execute(sql_query)

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id, 'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    res_record = database_api_utils.parse_sql_res(database_cursor)

    return database_api_response(record=res_record)


def add_lecture(req: add_lecture_request) -> database_api_response:
    func_id = f"{_MODULE_ID}.add_lecture"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    INSERT INTO lectures (lecture_name_en, lecture_name_ar, lecture_desc_en, lecture_desc_ar, thumbnail, price, duration)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    '''

    sql_vals = [
        req.lec_name_en,
        req.lec_name_ar,
        req.lec_desc_en,
        req.lec_desc_ar,
        req.thumbnail,
        req.price,
        req.duration,
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
        'lec_id': database_cursor.lastrowid,
    }])


def delete_lectures(req: delete_lectures_request) -> database_api_response:
    func_id = f"{_MODULE_ID}.delete_lectures"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    DELETE FROM lectures
    WHERE lecture_id IN (%s);
    ''' % (','.join(['%s' for _ in range(len(req.lec_ids))]))

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values {req.lec_ids}")

    try:
        database_cursor.execute(sql_query, req.lec_ids)
        database_connection.commit()

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id, 'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    return database_api_response(msg='OK')


def update_lecture(req: update_lecture_request) -> database_api_response:
    func_id = f"{_MODULE_ID}.update_lecture"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    UPDATE lectures
    SET
    lecture_name_en = %s,
    lecture_name_ar = %s,
    lecture_desc_en = %s,
    lecture_desc_ar = %s,
    thumbnail = %s,
    price = %s,
    duration = %s
    WHERE
    lecture_id = %s;
    '''

    sql_vals = [
        req.lec_name_en,
        req.lec_name_ar,
        req.lec_desc_en,
        req.lec_desc_ar,
        req.thumbnail,
        req.price,
        req.duration,
        req.lec_id,
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


def get_lecs_data_source() -> database_api_response:
    func_id = f"{_MODULE_ID}.get_lecs_data_source"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT
    l.lecture_name_en ,
    l.lecture_id 
    FROM lectures l;
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


def get_lecture_content_meta_data(lecture_id: int) -> database_api_response:
    func_id = f"{_MODULE_ID}.get_lecture_content_meta_data"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT
    m.material_name_en,
    m.material_name_ar,
    m.material_type
    FROM materials m
    WHERE lecture_id = %s;
    '''

    log_man.add_log(func_id,
                    'DEBUG', f"executing query {sql_query}, with values [{lecture_id}]")

    try:
        database_cursor.execute(sql_query, [lecture_id])

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id, 'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    res_record = database_api_utils.parse_sql_res(database_cursor)
    return database_api_response(record=res_record)
