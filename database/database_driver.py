import mysql.connector
import lib.log as log_man


_MODULE_ID = 'database.database_driver'


def get_database_connection() -> tuple[mysql.connector.MySQLConnection, mysql.connector.connection.MySQLCursor]:
    func_id = f"{_MODULE_ID}.get_database_connection"
    database_connection = None
    database_cursor = None

    log_man.add_log(func_id, 'DEBUG', 'creating a database connection')

    # connection config
    server_addr = '127.0.0.1'
    database_name = 'the_concept_academy'
    user_name = 'root'
    password = 'p@55word'
    try:
        conn = mysql.connector.connect(
            host=server_addr,
            user=user_name,
            password=password,
            database=database_name
        )
        database_connection = conn
        database_cursor = conn.cursor()

    except Exception as err:
        err_msg = f"database connection error: {err}"
        log_man.add_log(func_id, 'ERROR', err_msg)
        raise err

    return (database_connection, database_cursor)
