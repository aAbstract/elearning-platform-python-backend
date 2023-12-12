def map_sql_params(sql_params):
    return {
        'sql_keys': ','.join([key for key in sql_params.keys()]),
        'sql_vals': [sql_params[key] for key in sql_params.keys()],
        'sql_str': ','.join(['%s' for _ in sql_params.keys()])
    }


def parse_sql_res(cursor):
    # fetch record column names
    col_names = [column[0] for column in cursor.description]
    out_rec = []
    for record in cursor.fetchall():
        out_obj = {}
        for i in range(len(col_names)):
            out_obj[col_names[i]] = record[i]
        out_rec.append(out_obj)
    return out_rec
