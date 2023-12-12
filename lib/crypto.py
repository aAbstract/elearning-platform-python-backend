import hmac
import hashlib

import lib.settings as set_man


# module config
_hmac_key: str = set_man.get_settings('hmac_key')


def hash_password(password: str) -> str:
    return hmac.new(_hmac_key.encode(), password.encode(), hashlib.sha512).hexdigest()
