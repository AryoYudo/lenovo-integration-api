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

router = APIRouter()
secret_key = secrets.token_hex(32)

# Login
class LoginRequest(BaseModel):
    username: str
    password: str
    device_name: str
    station_name: str

# Json Insert Incoming Part
class ScanRequest(BaseModel):
    scan_item: str
    data_name: str
    qty_per_batch: int

# Json Insert Check Ressult Batch
class SaveDataItem(BaseModel):
    data_name: str
    data_value: str

class ScanItemData(BaseModel):
    data_name: str
    scan_item: str
    save_data: List[SaveDataItem] = []

class SaveDataBatch(BaseModel):
    data_name: str
    data_value: List[ScanItemData]

class InsertPayload(BaseModel):
    scan_item: str 
    data_name: str
    device_name: str
    station_name: str
    save_data: List[SaveDataBatch]

# Json Insert TesT Result Batch
class SaveDataItemTest(BaseModel):
    data_name: str
    data_value: str

class ScanItemDataTest(BaseModel):
    data_name: str
    scan_item: str
    save_data: List[SaveDataItemTest] = []

class SaveDataTestResultBatch(BaseModel):
    data_name: str
    data_value: List[ScanItemDataTest]

class InsertTestResultBatch(BaseModel):
    key_item: str
    device_name: str
    station_name: str
    is_pass: bool
    log_path: str
    save_data: List[SaveDataTestResultBatch]
    work_order_no: str
    scan_item: str 

@router.post("/sfis/login")
async def login(request: LoginRequest):
    try:
        data_to_send = request.dict()
        response = requests.post(LOGIN, json=data_to_send)
        response.raise_for_status()
        
        user_data = response.json()
        
        return JSONResponse(status_code=200, content={ "status": "success", "message": "Login successfully!", "data": user_data })
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Terjadi kesalahan: {str(e)}")
    
@router.post("/sfis/insert_incoming_part")
def scan_item(request: ScanRequest, Authorization: str = Header(None)):
    try:
        if not Authorization:
            raise HTTPException(status_code=401, detail="Authorization tidak ditemukan, silakan login dulu. ")
        
        data_to_send = request.dict()
        token_auth = 'token' + Authorization

        response = requests.post(
            INSERT_INCOMING_PART_BATCH,
            json=data_to_send,
            headers={"Authorization": token_auth, "Content-Type": "application/json"}
        )

        return JSONResponse(status_code=200, content={ "status": "success", "message": "Data successfully added to API!", "data": response.json(), })
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e)) 

@router.post("/sfis/insert_check_route_batch")
async def insert_check_route_batch(payload: InsertPayload, Authorization: str = Header(None)):
    try:
        if not Authorization:
            raise HTTPException(status_code=401, detail="Authorization tidak ditemukan, silakan login dulu. ")
        
        data_to_send = payload.dict()
        token_auth = 'token '+ Authorization

        response = requests.post(
            CHECK_ROUTE_BATCH, 
            json=data_to_send,
            headers={"Authorization": token_auth, "Content-Type": "application/json"}
        )

        return JSONResponse(status_code=200, content={ "status": "success", "message": "Data successfully added to API!", "data": response.json(), })
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/sfis/insert_test_result_batch")
async def insert_test_result_batch(payload: InsertTestResultBatch, Authorization: str = Header(None)):
    try:
        data_to_send = payload.dict()
        token_auth = 'token '+ Authorization

        response = requests.post(
            INSERT_TEST_RESULT_BATCH, 
            json=data_to_send,
            headers={"Authorization": token_auth, "Content-Type": "application/json"}
        )

        return JSONResponse(status_code=200, content={ "status": "success", "message": "Data successfully added to API!", "data": response.json(), })
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))



    
