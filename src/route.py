from fastapi import HTTPException, Request, APIRouter
from fastapi.responses import JSONResponse
import json
from src.config import LOGIN, INSERT_RESULT, INSERT_CHECK
from src.config import USERNAME, PASSWORD
from pydantic import BaseModel
from src.pydantic_models import CheckRouteRequest, InsertSolderRequest
from src.helpers import get_token, mes_api_call_wrapper
import secrets
import requests

router = APIRouter()
secret_key = secrets.token_hex(32)

@router.post("/insert_check_router")
async def insert_check_router(request: Request, json_body: CheckRouteRequest):
    token = get_token(json_body)
    token_auth = 'token ' + token

    check_route = {
        "scan_item": json_body.key_item,
        "data_name": json_body.data_name,
        "device_name": json_body.device_name,
        "station_name": json_body.station_name
    }
    checkroute_resp = mes_api_call_wrapper(INSERT_CHECK, json=check_route, headers={"Authorization": token_auth, "Content-Type": "application/json"})

    if checkroute_resp.json()['success']:
        test_result = {
            "key_item": json_body.key_item,
            "station_name": json_body.station_name,
            "device_name": json_body.device_name,
            "is_pass": json_body.is_pass,
            "error_code": json_body.error_code,
            "log_path": json_body.log_path,
            "log_data": json_body.log_data,
        }
        insert_resp = mes_api_call_wrapper(INSERT_RESULT, json=test_result, headers={"Authorization": token_auth, "Content-Type": "application/json"})
        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": "Data successfully added to API!", "data": insert_resp.json()})