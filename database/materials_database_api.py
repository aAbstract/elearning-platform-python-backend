from models.internal.database_api import database_api_response
from models.web.admin.materials_requests import add_vid_doc_request, delete_materials_request, update_vid_doc_request, add_quiz_request, update_quiz_request

import database.database_driver as database_driver
import database.database_api_utils as database_api_utils
import lib.log as log_man


# module config
_MODULE_ID = 'database.lectures_database_api'


def get_all_materials() -> database_api_response:
    func_id = f"{_MODULE_ID}.get_all_materials"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT
    m.material_id ,
    m.lecture_id ,
    l.lecture_name_en ,
    m.material_type ,
    m.material_order ,
    m.material_name_en ,
    m.material_name_ar ,
    m.material_link
    FROM materials m
    INNER JOIN lectures l
    ON m.lecture_id = l.lecture_id;
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


def add_vid_doc_mat(req: add_vid_doc_request) -> database_api_response:
    func_id = f"{_MODULE_ID}.add_vid_doc_mat"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    INSERT INTO materials (lecture_id, material_type, material_order, material_name_en, material_name_ar, material_link)
    VALUES (%s, %s, %s, %s, %s, %s);
    '''

    sql_vals = [
        req.linked_lec_id,
        req.mat_type,
        req.mat_order,
        req.mat_name_en,
        req.mat_name_ar,
        req.mat_link,
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
        'mat_id': database_cursor.lastrowid,
    }])


def delete_materials(req: delete_materials_request) -> database_api_response:
    func_id = f"{_MODULE_ID}.delete_materials"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    DELETE FROM materials
    WHERE material_id IN (%s);
    ''' % (','.join(['%s' for _ in range(len(req.items))]))

    sql_vals = list(map(lambda x: x.mat_id, req.items))

    log_man.add_log(
        func_id, 'DEBUG', f"executing query {sql_query}, with values {sql_vals}")

    try:
        database_cursor.execute(sql_query, sql_vals)
        database_connection.commit()

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id, 'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    return database_api_response(msg='OK')


def update_vid_doc(req: update_vid_doc_request) -> database_api_response:
    func_id = f"{_MODULE_ID}.update_vid_doc"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    UPDATE materials
    SET
    lecture_id = %s,
    material_type = %s,
    material_order = %s,
    material_name_en = %s,
    material_name_ar = %s,
    material_link = %s
    WHERE
    material_id = %s;
    '''

    sql_vals = [
        req.linked_lec_id,
        req.mat_type,
        req.mat_order,
        req.mat_name_en,
        req.mat_name_ar,
        req.mat_link,
        req.mat_id,
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


def get_mat_info(mat_id: int) -> database_api_response:
    func_id = f"{_MODULE_ID}.get_mat_info"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    SELECT *
    FROM materials
    WHERE material_id = %s;
    '''

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values [{mat_id}]")

    try:
        database_cursor.execute(sql_query, [mat_id])

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id, 'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    res_record = database_api_utils.parse_sql_res(database_cursor)

    return database_api_response(record=res_record)


def add_quiz_mat(req: add_quiz_request) -> database_api_response:
    func_id = f"{_MODULE_ID}.add_quiz_mat"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    # add quiz material entry
    sql_query = '''
    INSERT INTO materials (lecture_id, material_type, material_order, material_name_en, material_name_ar, material_link)
    VALUES (%s, %s, %s, %s, %s, %s);
    '''

    sql_vals = [
        req.linked_lec_id,
        req.mat_type,
        req.mat_order,
        req.mat_name_en,
        req.mat_name_ar,
        req.mat_link,
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

    # add answers entry
    mat_id = database_cursor.lastrowid

    for ans in req.quiz_answers:
        sql_query = '''
        INSERT INTO quiz_answers (material_id, question_order, answer_char)
        VALUES (%s, %s, %s);
        '''

        sql_vals = [
            mat_id,
            ans.question_order,
            ans.question_answer,
        ]

        log_man.add_log(func_id, 'DEBUG',
                        f"executing query {sql_query}, with values {sql_vals}")

        try:
            database_cursor.execute(sql_query, sql_vals)

        except Exception as err:
            err_msg = f"database error: {err}"
            log_man.add_log(func_id,
                            'ERROR', err_msg)

            return database_api_response(success=False, msg=err_msg)

    database_connection.commit()
    return database_api_response(record=[{
        'mat_id': mat_id,
    }])


def update_quiz(req: update_quiz_request) -> database_api_response:
    func_id = f"{_MODULE_ID}.update_quiz"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    # update material entry
    sql_query = '''
    UPDATE materials
    SET
    lecture_id = %s,
    material_type = %s,
    material_order = %s,
    material_name_en = %s,
    material_name_ar = %s,
    material_link = %s
    WHERE
    material_id = %s;
    '''

    sql_vals = [
        req.linked_lec_id,
        req.mat_type,
        req.mat_order,
        req.mat_name_en,
        req.mat_name_ar,
        req.mat_link,
        req.mat_id,
    ]

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values {sql_vals}")

    try:
        database_cursor.execute(sql_query, sql_vals)

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id, 'ERROR', err_msg)

        return database_api_response(success=False, msg=err_msg)

    # update quiz answers entry (remove old answers)
    sql_query = '''
    DELETE FROM quiz_answers
    WHERE material_id = %s;
    '''

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values {[req.mat_id]}")

    try:
        database_cursor.execute(sql_query, [req.mat_id])

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id, 'ERROR', err_msg)

        return database_api_response(success=False, msg=err_msg)

    # update quiz answers entry (add new answers)
    for ans in req.quiz_answers:
        sql_query = '''
        INSERT INTO quiz_answers (material_id, question_order, answer_char)
        VALUES (%s, %s, %s);
        '''

        sql_vals = [
            req.mat_id,
            ans.question_order,
            ans.question_answer,
        ]

        log_man.add_log(func_id, 'DEBUG',
                        f"executing query {sql_query}, with values {sql_vals}")

        try:
            database_cursor.execute(sql_query, sql_vals)

        except Exception as err:
            err_msg = f"database error: {err}"
            log_man.add_log(func_id,
                            'ERROR', err_msg)

            return database_api_response(success=False, msg=err_msg)

    database_connection.commit()
    return database_api_response(msg='OK')
