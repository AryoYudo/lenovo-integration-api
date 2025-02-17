from fastapi import FastAPI, Depends, HTTPException, Request, Header, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from api import LOGIN, INSERT_RESULT_PCB, INSERT_CHECK_PCB, INSERT_INCOMING_PART_BATCH, CHECK_ROUTE_BATCH, INSERT_TEST_RESULT_BATCH, GET_VERSION
from typing import List
from config import IS_LIVE
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
            "username": "11",
            "password": "11",
            "device_name": "USB_HUB_10003_A",
            "station_name": "ROUTING_MPCBA"
        }

    response = requests.post(LOGIN, json=login_payload)

    if response.status_code == 200:
        token_data = response.json()
        token_cache["token"] = token_data.get("token")
        token_cache["expires_at"] = time.time() + 3600  # Misal token berlaku 1 jam (3600 detik)
        return token_cache["token"]

    raise HTTPException(status_code=401, detail="Login failed, unable to retrieve token")

@router.post("/insert_check_router")
async def insert_check_router(request: Request):
    try:
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
        checkroute_resp.raise_for_status()
        
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
            insert_resp.raise_for_status()

            return JSONResponse(
                status_code=200,
                content={"status": "success", "message": "Data successfully added to API!", "data": checkroute_resp.json()})
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

 
@router.post("/insert_solder")
async def scan_item(request: Request):
    try:
        json_body = await request.json()
        token = get_token(json_body)
        if not token:
            raise HTTPException(status_code=401, detail="Token tidak ditemukan, silakan login dulu. ")
        token_auth = 'token ' + token

        incoming_data = {
            "scan_item": json_body.get("scan_item"),
            "data_name": json_body.get("data_name"),
            "qty_per_batch": json_body.get("qty_per_batch")
        }
        response_incoming = requests.post(INSERT_INCOMING_PART_BATCH, json=incoming_data, headers={"Authorization": token_auth, "Content-Type": "application/json"})
        response_json = response_incoming.json()

        check_data = []
        test_data = []

        if response_json.get("success") and "save_data" in response_json:
            for item in response_json["save_data"].get("scan_items", []):
                data_version_url = f"{GET_VERSION}?scan_item={item.get('scan_item')}"
                data_version_response = requests.get(data_version_url)
                data_version = data_version_response.json()

                check_route_data = {
                    "scan_item": item.get("scan_item"),
                    "data_name": item.get("data_name"),
                    "device_name": json_body.get("device_name"),
                    "station_name": json_body.get("station_name"),
                    "save_data": item.get("save_data", [])
                }
                check_data.append(check_route_data)

                test_result_data = {
                    "key_item": json_body.get("key_item"),
                    "device_name": json_body.get("device_name"),
                    "station_name": json_body.get("station_name"),
                    "is_pass": json_body.get("is_pass"),
                    "log_path": json_body.get("log_path"),
                    "work_order_no": data_version.get("work_order_no"),
                    "scan_item": item.get("scan_item"),
                    "save_data": item.get("save_data", [])
                }
                test_data.append(test_result_data)

        response_check_route = requests.post(CHECK_ROUTE_BATCH, json=check_data, headers={"Authorization": token_auth, "Content-Type": "application/json"})
        response_test_result = requests.post(INSERT_TEST_RESULT_BATCH, json=test_data, headers={"Authorization": token_auth, "Content-Type": "application/json"})

        return JSONResponse(status_code=200, content={"status": "success", "message": "Data successfully added to API!", "data_incoming": response_json, "data_check": response_check_route.json(), "data_result": response_test_result.json()})
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

