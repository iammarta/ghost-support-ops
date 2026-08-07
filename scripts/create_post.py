import jwt
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["GHOST_ADMIN_API_KEY"]
API_URL = os.environ["GHOST_API_URL"]

id, secret = API_KEY.split(':')

iat = int(time.time())
header = {'alg': 'HS256', 'typ': 'JWT', 'kid': id}
payload = {
    'iat': iat,
    'exp': iat + 5 * 60,
    'aud': '/admin/'
}
token = jwt.encode(payload, bytes.fromhex(secret), algorithm='HS256', headers=header)

url = f"{API_URL}/ghost/api/admin/posts/"
headers = {
    'Authorization': f'Ghost {token}',
    'Content-Type': 'application/json'
}
body = {
    "posts": [{
        "title": "Created via Admin API",
        "status": "draft",
        "lexical": '{"root":{"children":[{"children":[{"detail":0,"format":0,"mode":"normal","style":"","text":"This post was created programmatically via the Ghost Admin API.","type":"extended-text","version":1}],"direction":"ltr","format":"","indent":0,"type":"paragraph","version":1}],"direction":"ltr","format":"","indent":0,"type":"root","version":1}}'
    }]
}

response = requests.post(url, headers=headers, json=body)
print(response.status_code)
print(response.json())