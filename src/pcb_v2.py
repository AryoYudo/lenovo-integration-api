from fastapi import HTTPException, Request, APIRouter
from fastapi.responses import JSONResponse

from src.config import LOGIN, INSERT_RESULT_PCB, INSERT_CHECK_PCB, INSERT_INCOMING_PART_BATCH, CHECK_ROUTE_BATCH, INSERT_TEST_RESULT_BATCH, GET_VERSION
from src.config import USERNAME, PASSWORD
import time
import secrets
import requests

router = APIRouter()
secret_key = secrets.token_hex(32)
token_cache = {"token": None, "expires_at": 0}


def mes_api_call_wrapper(url, json, headers=None):
    print('[CALL API]', url)
    print('[API INPUT]', json)
    if headers:
        mes_resp = requests.post(url, json=json, headers=headers)
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


@router.post("/insert_solder_prod")
async def insert_solder_prod(request: Request):
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
        print('incoming data', incoming_data)
        response_incoming = requests.post(INSERT_INCOMING_PART_BATCH, json=incoming_data, headers={"Authorization": token_auth, "Content-Type": "application/json"})
        print('incoming content:', json.dumps(response_incoming.json(), indent=4))
        print('incoming done')
        response_incoming_json = response_incoming.json()
        if response_incoming.status_code >= 400:
            raise HTTPException(response_incoming.status_code, detail=response_incoming_json.get("message", "Unkown Error"))

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
            print('checkroute data', json.dumps(check_data, indent=4))
            response_check_route = requests.post(CHECK_ROUTE_BATCH, json=check_data,
                                                 headers={"Authorization": token_auth, "Content-Type": "application/json"})
            print('checkroute content:', json.dumps(response_check_route.json(), indent=4))

            if response_check_route.status_code >= 400:
                raise HTTPException(response_check_route.status_code, detail=response_check_route.json().get("message", "Unkown Error"))

            print('checkroute done')
            if response_check_route.json().get('success', False):
                data_version_url = f"{GET_VERSION}?scan_item={json_body.get('scan_item')}"
                print('data_version_url:', data_version_url)
                data_version_response = requests.get(data_version_url)
                print('data_version_response :', json.dumps(data_version_response.json(), indent=4))

                if data_version_response.status_code >= 400:
                    raise HTTPException(data_version_response.status_code,
                                        detail=str(data_version_response.json()))

                # data_version_response.raise_for_status()
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
                print('test_data :', json.dumps(test_data, indent=4))
                response_test_result = requests.post(INSERT_TEST_RESULT_BATCH, json=test_data, headers={"Authorization": token_auth, "Content-Type": "application/json"})
                print('insert content:', json.dumps(response_test_result.json(), indent=4))
                if response_test_result.status_code >= 400:
                    raise HTTPException(response_test_result.status_code,
                                        detail=response_test_result.json().get("message", "Unkown Error"))
                print('insert result done')
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
        response_json = e.response.json()
        message1 = response_json.get("detail")
        message2 = response_json.get("message")
        raise HTTPException(status_code=e.response.status_code, detail=f"{message1}{message2}")