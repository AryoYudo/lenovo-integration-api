from fastapi import FastAPI, Depends, HTTPException, Request, Header, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .api_mes import INSERT_RESULT_PCB, INSERT_CHECK_PCB
from typing import List
import jwt
import httpx
import datetime
import uuid
import secrets
import requests
import os

# app = FastAPI()
router = APIRouter()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
secret_key = secrets.token_hex(32)

# Insert untuk Test Result Mas Sena
class InsertTestResult(BaseModel):
    key_item: str
    station_name: str
    device_name: str
    is_pass: str
    error_code: str
    log_path: str
    log_data: str

class InsertCheckRoute(BaseModel):
    scan_item: str
    data_name: str
    device_name: str
    station_name: str   

@router.post("/sfis/insert_check_router")
async def insert_check_router(payload: InsertCheckRoute):
    try:
        data_to_send = payload.dict()
        
        response = requests.post(
            INSERT_CHECK_PCB, 
            json=data_to_send,
            headers={"Content-Type": "application/json"}
        )

        return JSONResponse(status_code=200, content={ "status": "success", "message": "Data successfully added to API!", "data": response.json(), })
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sfis/insert_test_result")
async def insert_test_result(payload: InsertTestResult):
    try:
        data_to_send = payload.dict()

        response = requests.post(
            INSERT_RESULT_PCB, 
            json=data_to_send,
            headers={"Content-Type": "application/json"}
        )

        return JSONResponse(status_code=200, content={ "status": "success", "message": "Data successfully added to API!", "data": response.json(), })
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))