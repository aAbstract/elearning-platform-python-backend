import requests
import json

admin_access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoxLCJmdWxsX25hbWUiOiJBaG1lZCBIZXNoYW0iLCJ1c2VybmFtZSI6ImFoZXNoYW0iLCJ1c2VyX3JvbGUiOiJBRE1JTiIsInVzZXJfaW1nIjoiaW1nX2F2YXRhci5wbmcifQ.K22WD8Wy-r3MzlQAn7EZq2X6zV-faPb3-Gt9BKP-1zzOptPm088mhD36I0Ht7bHmJ2nuBOELf3Z1ICBhTWQP_g'

headers = {
    'Authorization': f"Bearer {admin_access_token}",
}

api_url = 'http://127.0.0.1:8080/api/admin/users/get-user-info'

json_body = {
    'username': 'testuserx',
}

http_res = requests.post(api_url, json=json_body, headers=headers)
json_body = json.loads(http_res.content.decode())
print(json.dumps(json_body, indent=2))
