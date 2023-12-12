import requests
import json


_server_url = '127.0.0.1'
_server_port = 8080

ssl_verify = False


def get_server_url():
    return f"http://{_server_url}:{_server_port}"


def login_user(username: str, password: str) -> str:
    server_url = get_server_url()
    api_url = f"{server_url}/api/auth/login"

    json_body = {
        'username': username,
        'password': password,
    }

    http_resp = requests.post(api_url, json=json_body)

    json_obj = json.loads(http_resp.content.decode())

    return json_obj
