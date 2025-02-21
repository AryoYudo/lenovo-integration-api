import time
import requests  
from fastapi import HTTPException  
from src.config import USERNAME, PASSWORD

token_cache = {"token": None, "expires_at": 0}
def get_token(json_body):
    """Mengambil token dari cache atau login jika expired"""
    global token_cache

    if token_cache["token"] and token_cache["expires_at"] > time.time():
        return token_cache["token"]

    login_payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "device_name": json_body.get('device_name'),
        "station_name": json_body.get('station_name')
    }
    response = mes_api_call_wrapper(LOGIN, json=login_payload)

    token_data = response.json()
    token_cache["token"] = token_data.get("token")
    token_cache["expires_at"] = int(time.time()) + 3600  
    return token_cache["token"]

def mes_api_call_wrapper(url, json=None, headers=None, is_get=False):
    print('[CALL API]', url)
    print('[API INPUT]', json)
    if headers:
        if is_get:
            mes_resp = requests.get(url, headers=headers)
        else:
            mes_resp = requests.post(url, json=json, headers=headers)
    else:
        if is_get:
            mes_resp = requests.get(url)
        else:
            mes_resp = requests.post(url, json=json)

    print('[API OUTPUT]', mes_resp.text)
    if mes_resp.status_code != 200:
        try:
            error_msg = f"[{url}] {mes_resp.json().get('message')}"
        except Exception as e:
            error_msg = f"[{url}] {mes_resp.text}"
        raise HTTPException(status_code=mes_resp.status_code, detail=error_msg)
    return mes_resp