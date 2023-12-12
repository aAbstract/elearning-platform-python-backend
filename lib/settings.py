import json

import lib.log as log_man

# module config
_settings_file_dir = './settings.json'
_MODULE_ID = 'lib.settings'

# module state
_settings_obj = None


def _init_module():
    func_id = f"{_MODULE_ID}._init_module"

    global _settings_obj

    log_man.add_log(func_id, 'DEBUG',
                    f"loading settings file: {_settings_file_dir}")

    try:
        with open(_settings_file_dir, 'r') as f:
            set_json_txt = f.read()
            _settings_obj = json.loads(set_json_txt)

        log_man.add_log(func_id, 'DEBUG',
                        f"done loading settings file: {_settings_file_dir}")

    except Exception as err:
        log_man.add_log(func_id, 'ERROR', f"error loading settings file {err}")


def get_settings(setting_key: str):
    return _settings_obj[setting_key]


_init_module()
