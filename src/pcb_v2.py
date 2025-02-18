from fastapi import HTTPException, Request, APIRouter
from fastapi.responses import JSONResponse

from src.config import LOGIN, INSERT_RESULT_PCB, INSERT_CHECK_PCB, INSERT_INCOMING_PART_BATCH, CHECK_ROUTE_BATCH, INSERT_TEST_RESULT_BATCH, GET_VERSION
from src.config import IS_LIVE, USERNAME, PASSWORD
import time
import secrets
import requests

router = APIRouter()
secret_key = secrets.token_hex(32)
token_cache = {"token": None, "expires_at": 0}

def get_token(json_body):
    """Mengambil token dari cache atau login jika expired"""
    global token_cache

    # Jika token masih valid, gunakan token yang sudah ada
    if token_cache["token"] and token_cache["expires_at"] > time.time():
        return token_cache["token"]

    # Jika token expired atau tidak ada, lakukan login ulang
    if not IS_LIVE:
        login_payload = {
            "username": "test",            
            "password": "11",              
            "device_name": "DSY_Test_1002", 
            "station_name": "Autoscrew"     
        }
    else:
        login_payload = {
            "username": USERNAME,
            "password": PASSWORD,
            "device_name": json_body.get('device_name'),
            "station_name": json_body.get('station_name')
        }
    print('LOGIN: ',login_payload)
    response = requests.post(LOGIN, json=login_payload)
    print('LOGIN RESP:', response.content)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.content)

    token_data = response.json()
    token_cache["token"] = token_data.get("token")
    token_cache["expires_at"] = int(time.time()) + 36  # Misal token berlaku 1 jam (3600 detik)
    return token_cache["token"]


@router.post("/insert_check_router")
async def insert_check_router(request: Request):
    json_body = await request.json()
    print('JSON_BODY', json_body)
    token = get_token(json_body)
    token_auth = 'token ' + token

    check_route = {
        "scan_item": json_body.get("key_item"),
        "data_name": json_body.get("data_name"),
        "device_name": json_body.get("device_name"),
        "station_name": json_body.get("station_name")
    }
    print('check_route', check_route)
    checkroute_resp = requests.post(INSERT_CHECK_PCB, json=check_route, headers={"Authorization": token_auth, "Content-Type": "application/json"})
    print('checkroute_resp', checkroute_resp.content)
    if checkroute_resp.status_code != 200:
        raise HTTPException(status_code=checkroute_resp.status_code, detail=checkroute_resp.content)

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
        print('test_result', test_result)
        insert_resp = requests.post(INSERT_RESULT_PCB, json=test_result, headers={"Authorization": token_auth, "Content-Type": "application/json"})
        print('insert_resp', insert_resp.content)
        if insert_resp.status_code != 200:
            raise HTTPException(status_code=insert_resp.status_code, detail=insert_resp.content)

        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": "Data successfully added to API!", "data": checkroute_resp.json()})


@router.post("/insert_solder")
async def insert_solder_maftuh(request: Request):
    try:
        json_body = await request.json()
        token = get_token(json_body)
        if not token:
            raise HTTPException(status_code=401, detail="Token tidak ditemukan, silakan login dulu. ")
        token_auth = 'token ' + token

        incoming_data = {
            "scan_item": json_body.get("scan_item"),
            "data_name": 'J69_ADAPT_PCBA',
            "qty_per_batch": json_body.get("qty_per_batch")
        }

        response_incoming = requests.post(INSERT_INCOMING_PART_BATCH, json=incoming_data, headers={"Authorization": token_auth, "Content-Type": "application/json"})
        response_incoming.raise_for_status()
        response_incoming_json = response_incoming.json()
        
        if 'save_data' in response_incoming_json:
            save_data = response_incoming_json.get("save_data", {})
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
            response_check_route = requests.post(CHECK_ROUTE_BATCH, json=check_data,
                                                 headers={"Authorization": token_auth, "Content-Type": "application/json"})
            response_check_route.raise_for_status()
            
            if response_check_route.json().get('success', False):
                data_version_url = f"{GET_VERSION}?scan_item={json_body.get('scan_item')}"
                data_version_response = requests.get(data_version_url)

                data_version_response.raise_for_status()
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

                response_test_result = requests.post(INSERT_TEST_RESULT_BATCH, json=test_data, headers={"Authorization": token_auth, "Content-Type": "application/json"})
                response_test_result.raise_for_status()
                return JSONResponse(status_code=200,
                                    content={"status": "success", "message": "Data successfully added to API!",
                                             "data_incoming": response_incoming_json, "data_check": response_check_route.json(),
                                             "data_result": response_test_result.json()})
            else:
                return JSONResponse(status_code=200,
                                    content={"status": "success", "message": "FAIL check route",
                                             "data_incoming": response_incoming_json, "data_check": response_check_route.json(),
                                             })
        else:
            return JSONResponse(status_code=200,
                                content={"status": "success", "message": "FAIL get family",
                                         "data_incoming": response_incoming_json})
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))


