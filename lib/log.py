from pydantic import BaseModel
from datetime import datetime
import colorama


class log(BaseModel):
    ''' log data model '''

    date: datetime
    level: str
    mod_id: str  # module id
    description: str  # log content


# module config
allow_filter = ['ERROR', 'INFO', 'DEBUG']
log_tag_color_map = {
    'ERROR': f"{colorama.Back.RED}[ERROR]{colorama.Style.RESET_ALL}",
    'INFO': '[INFO]',
    'DEBUG': '[DEBUG]',
}

# module state
logs: list[log] = []


def _format_log(log_obj: log):
    return f"[{log_obj.date.strftime('%Y-%m-%d %H:%M:%S')}] {log_tag_color_map[log_obj.level]} [{log_obj.mod_id}] | {log_obj.description}"


def add_log(mod_id: str, level: str, desc: str):
    ''' this fucntion addes info level log to the log buffer '''

    global logs

    temp_log_obj = log(
        date=datetime.now(),
        level=level,
        mod_id=mod_id,
        description=desc
    )

    if level in allow_filter:
        formated_log = _format_log(temp_log_obj)
        print(formated_log)

    logs.append(temp_log_obj)

    # clear logs memory buffer when needed
    if len(logs) == 2000:
        log_buffer = ''
        err_log_buffer = ''

        for log_item in logs:
            log_buffer += _format_log(log_item)
            log_buffer += f"\n{'='*200}\n"

            if log_item.level == 'ERROR':
                err_log_buffer += _format_log(log_item)
                err_log_buffer += f"\n{'='*200}\n"

        with open('./backups/logs.txt', 'a') as f:
            f.write(log_buffer)

        with open('./backups/err_logs.txt', 'a') as f:
            f.write(err_log_buffer)

        logs.clear()
