from fastapi import FastAPI, Depends, HTTPException, Request, Header, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .api_mes import LOGIN, INSERT_INCOMING_PART_BATCH, CHECK_ROUTE_BATCH, INSERT_TEST_RESULT_BATCH
from typing import List
import jwt
import httpx
import datetime
import uuid
import secrets
import requests
import os
import time

router = APIRouter()
secret_key = secrets.token_hex(32)
token_cache = {"token": None, "expires_at": 0}

def get_token(json_body):
    global token_cache
    if token_cache["token"] and token_cache["expires_at"] > time.time():
        return token_cache["token"]

    login_payload = {
        "username": "test",            
        "password": "11",              
        "device_name": "DSY_Test_1002", 
        "station_name": "Autoscrew"     
    }
    response = requests.post(LOGIN, json=login_payload)

    if response.status_code == 200:
        token_data = response.json()
        token_cache["token"] = token_data.get("token")
        token_cache["expires_at"] = time.time() + 3600 
        return token_cache["token"]
    raise HTTPException(status_code=401, detail="Login failed, unable to retrieve token")

    
@router.post("/sfis/insert_incoming_part")
async def scan_item(request: Request):
    try:
        json_body = await request.json()
        token = get_token(json_body)
        if not token:
            raise HTTPException(status_code=401, detail="Token tidak ditemukan, silakan login dulu. ")
        token_auth = 'token ' + token

        data = {
            "scan_item": json_body.get("scan_item"),
            "data_name": json_body.get("data_name"),
            "qty_per_batch": json_body.get("qty_per_batch")
        }

        response = requests.post(INSERT_INCOMING_PART_BATCH, json=data, headers={"Authorization": token_auth, "Content-Type": "application/json"})

        return JSONResponse(status_code=200, content={ "status": "success", "message": "Data successfully added to API!", "data": response.json(), })
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e)) 


@router.post("/sfis/insert_check_route_batch")
async def insert_check_route_batch(request: Request):
    try:
        json_body = await request.json()
        token = get_token(json_body)
        if not token:
            raise HTTPException(status_code=401, detail="Token tidak ditemukan, silakan login dulu. ")
        token_auth = 'token '+ token

        data = {
            "scan_item": json_body.get("scan_item"),
            "data_name": json_body.get("data_name"),
            "device_name": json_body.get("device_name"),
            "station_name": json_body.get("station_name"),
            "save_data": json_body.get("save_data", [])
        }

        response = requests.post(
            CHECK_ROUTE_BATCH, 
            json=data,
            headers={"Authorization": token_auth, "Content-Type": "application/json"}
        )

        return JSONResponse(status_code=200, content={ "status": "success", "message": "Data successfully added to API!", "data": response.json(), })
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

    
@router.post("/sfis/insert_test_result_batch")
async def insert_test_result_batch(request: Request):
    try:
        json_body = await request.json()
        token = get_token(json_body)
        if not token:
            raise HTTPException(status_code=401, detail="Token tidak ditemukan, silakan login dulu.")
        token_auth = 'token '+ token

        data = {
            "key_item": json_body.get("key_item"),
            "device_name": json_body.get("device_name"),
            "station_name": json_body.get("station_name"),
            "is_pass": json_body.get("is_pass"),
            "log_path": json_body.get("log_path"),
            "work_order_no": json_body.get("work_order_no"),
            "scan_item": json_body.get("scan_item"),
            "save_data": json_body.get("save_data", [])
        }
    
        response = requests.post(
            INSERT_TEST_RESULT_BATCH, 
            json=data,
            headers={"Authorization": token_auth, "Content-Type": "application/json"}
        )

        return JSONResponse(status_code=200, content={ "status": "success", "message": "Data successfully added to API!", "data": response.json(), })
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))  
