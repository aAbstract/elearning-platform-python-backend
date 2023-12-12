from models.internal.database_api import database_api_response

import database.database_api_utils as database_api_utils
import database.database_driver as database_driver
import lib.log as log_man


# module config
_MODULE_ID = 'database.coupons_database_api'


def add_coupons_list(coupons_list: list[str], coupon_value: float) -> database_api_response:
    func_id = f"{_MODULE_ID}.add_coupons_list"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    INSERT INTO coupons (coupon_text, coupon_value)
    VALUES (%s, %s);
    '''

    for coupon in coupons_list:
        sql_vals = [coupon, coupon_value]

        log_man.add_log(func_id, 'DEBUG',
                        f"executing query {sql_query}, with values {sql_vals}")

        try:
            database_cursor.execute(sql_query, sql_vals)

        except Exception as err:
            err_msg = f"database error: {err}"
            log_man.add_log(func_id, 'ERROR', err_msg)
            return database_api_response(success=False, msg=err_msg)

    database_connection.commit()
    return database_api_response(msg='OK')


def get_all_coupons() -> database_api_response:
    func_id = f"{_MODULE_ID}.get_coupons_list"
    (_, database_cursor) = database_driver.get_database_connection()

    sql_query = 'SELECT * FROM coupons c;'

    log_man.add_log(func_id, 'DEBUG', f"executing query {sql_query}")

    try:
        database_cursor.execute(sql_query)

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id, 'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    res_record = database_api_utils.parse_sql_res(database_cursor)
    return database_api_response(record=res_record)


def delete_coupon_list(coupons_list: list[str]) -> database_api_response:
    func_id = f"{_MODULE_ID}.delete_coupon_list"
    (database_connection, database_cursor) = database_driver.get_database_connection()

    sql_query = '''
    DELETE FROM coupons
    WHERE coupon_text IN (%s);
    ''' % (','.join(['%s' for _ in range(len(coupons_list))]))

    log_man.add_log(func_id, 'DEBUG',
                    f"executing query {sql_query}, with values {coupons_list}")

    try:
        database_cursor.execute(sql_query, coupons_list)
        database_connection.commit()

    except Exception as err:
        err_msg = f"database error: {err}"
        log_man.add_log(func_id, 'ERROR', err_msg)
        return database_api_response(success=False, msg=err_msg)

    return database_api_response(msg='OK')
