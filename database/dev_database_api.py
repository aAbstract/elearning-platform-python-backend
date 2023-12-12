from models.internal.database_api import database_api_response

import database.database_driver as database_driver
import lib.log as log_man


# module config
_MODULE_ID = 'database.dev_database_api'


def update_database_connection() -> database_api_response:
    func_id = f"{_MODULE_ID}.update_database_connection"
    (database_connection, _) = database_driver.get_database_connection()

    try:
        database_connection.commit()

    except Exception as err:
        err_msg = f"database error: {err}"

        log_man.add_log(func_id, 'ERROR', err_msg)

        return database_api_response(success=False, msg=err_msg)

    log_man.add_log(func_id, 'DEBUG', 'database connection updated')

    return database_api_response(msg='OK')
