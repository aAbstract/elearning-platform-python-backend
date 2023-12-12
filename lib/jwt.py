from typing import Any
import jwt

import lib.settings as set_man


# module config
_jwt_key = set_man.get_settings('jwt_key')


# module API
def create_jwt_token(data: Any):
    return jwt.encode(data, _jwt_key, algorithm="HS512")


def decode_jwt_token(token: str):
    return jwt.decode(token, _jwt_key, algorithms=['HS512'])
