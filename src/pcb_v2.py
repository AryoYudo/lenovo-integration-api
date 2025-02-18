from fastapi import HTTPException, Request, APIRouter
from fastapi.responses import JSONResponse
import json

from src.config import LOGIN, INSERT_RESULT_PCB, INSERT_CHECK_PCB, INSERT_INCOMING_PART_BATCH, CHECK_ROUTE_BATCH, INSERT_TEST_RESULT_BATCH, GET_VERSION
from src.config import USERNAME, PASSWORD
import time
import secrets
import requests

router = APIRouter()
secret_key = secrets.token_hex(32)
token_cache = {"token": None, "expires_at": 0}


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


def get_token(json_body):
    """Mengambil token dari cache atau login jika expired"""
    global token_cache

    # Jika token masih valid, gunakan token yang sudah ada
    if token_cache["token"] and token_cache["expires_at"] > time.time():
        return token_cache["token"]

    login_payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "device_name": json_body.get('device_name'),
        "station_name": json_body.get('station_name')
    }
    # response = requests.post(LOGIN, json=login_payload)
    response = mes_api_call_wrapper(LOGIN, json=login_payload)

    token_data = response.json()
    token_cache["token"] = token_data.get("token")
    token_cache["expires_at"] = int(time.time()) + 3600  # Misal token berlaku 1 jam (3600 detik)
    return token_cache["token"]


@router.post("/insert_check_router")
async def insert_check_router(request: Request):
    json_body = await request.json()
    token = get_token(json_body)
    token_auth = 'token ' + token

    check_route = {
        "scan_item": json_body.get("key_item"),
        "data_name": json_body.get("data_name"),
        "device_name": json_body.get("device_name"),
        "station_name": json_body.get("station_name")
    }
    checkroute_resp = mes_api_call_wrapper(INSERT_CHECK_PCB, json=check_route, headers={"Authorization": token_auth, "Content-Type": "application/json"})

    if checkroute_resp.json()['success']:
        test_result = {
            "key_item": json_body.get("key_item"),
            "station_name": json_body.get("station_name"),
            "device_name": json_body.get("device_name"),
            "is_pass": json_body.get("is_pass"),
            "error_code": json_body.get("error_code"),
            "log_path": json_body.get("log_path"),
            "log_data": json_body.get("log_data"),
        }
        insert_resp = mes_api_call_wrapper(INSERT_RESULT_PCB, json=test_result, headers={"Authorization": token_auth, "Content-Type": "application/json"})
        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": "Data successfully added to API!", "data": insert_resp.json()})

@router.post("/insert_solder")
async def insert_solder(request: Request):
    json_body = await request.json()
    token = get_token(json_body)
    token_auth = 'token ' + token
    headers = {"Authorization": token_auth, "Content-Type": "application/json"}
    incoming_data = {
        "scan_item": json_body.get("scan_item"),
        "data_name": 'J69_ADAPT_PCBA',
        "qty_per_batch": json_body.get("qty_per_batch")
    }
    incoming_response = mes_api_call_wrapper(INSERT_INCOMING_PART_BATCH, json=incoming_data, headers=headers)
    incoming_response_json = incoming_response.json()
    save_data = incoming_response_json.get("save_data")
    if save_data is None:
        raise HTTPException(status_code=500, detail=str(incoming_response_json))

    save_data = [{
        "data_name": "scan_items",
        "data_value": save_data.get("scan_items", [])
    }]
    check_data = {
        "scan_item": json_body.get("scan_item"),
        "data_name": 'J69_ADAPT_PCBA',
        "device_name": json_body.get("device_name"),
        "station_name": json_body.get("station_name"),
        "save_data": save_data
    }
    check_route_response = mes_api_call_wrapper(CHECK_ROUTE_BATCH, json=check_data, headers=headers)
    check_route_response_json = check_route_response.json()
    if not check_route_response_json.get("success", False):
        raise HTTPException(status_code=check_route_response.status_code, detail=str(check_route_response.json()))

    data_version_url = f"{GET_VERSION}?scan_item={json_body.get('scan_item')}"
    data_version_response = mes_api_call_wrapper(data_version_url, is_get=True)

    if data_version_response.status_code != 200:
        raise HTTPException(status_code=data_version_response.status_code, detail=str(data_version_response.json()))

    work_order_no = data_version_response.json().get("work_order_no")
    test_data = {
        "key_item": json_body.get("key_item"),
        "device_name": json_body.get("device_name"),
        "station_name": json_body.get("station_name"),
        "is_pass": json_body.get("is_pass"),
        "log_path": json_body.get("log_path", ""),
        "work_order_no": work_order_no,
        "scan_item": json_body.get('scan_item'),
        "save_data": save_data,
        "error_code": '99999',
    }

    test_result_response = mes_api_call_wrapper(INSERT_TEST_RESULT_BATCH, json=test_data, headers=headers)
    if test_result_response.status_code != 200:
        raise HTTPException(status_code=test_result_response.status_code, detail=str(test_result_response.json()))

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Data successfully added to API!",
            "data_incoming": incoming_response_json,
            "data_check": check_route_response_json,
            "data_result": test_result_response.json()
        }
    )
