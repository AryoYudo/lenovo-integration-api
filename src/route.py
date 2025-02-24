from fastapi import HTTPException, Request, APIRouter
from fastapi.responses import JSONResponse
import json
from src.config import LOGIN, INSERT_RESULT_PCB, INSERT_CHECK_PCB, INSERT_INCOMING_PART_BATCH, CHECK_ROUTE_BATCH, INSERT_TEST_RESULT_BATCH, GET_VERSION
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
    checkroute_resp = mes_api_call_wrapper(INSERT_CHECK_PCB, json=check_route, headers={"Authorization": token_auth, "Content-Type": "application/json"})

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
        insert_resp = mes_api_call_wrapper(INSERT_RESULT_PCB, json=test_result, headers={"Authorization": token_auth, "Content-Type": "application/json"})
        return JSONResponse(
            status_code=200,
            content={"status": "success", "message": "Data successfully added to API!", "data": insert_resp.json()})

# @router.post("/insert_solder")
# async def insert_solder(request: Request, json_body: InsertSolderRequest):
#     token = get_token(json_body)
#     token_auth = 'token ' + token
#     headers = {"Authorization": token_auth, "Content-Type": "application/json"}

#     incoming_data = {
#         "scan_item": json_body.scan_item,
#         "data_name": 'J69_ADAPT_PCBA',
#         "qty_per_batch": json_body.qty_per_batch
#     }

#     incoming_response = mes_api_call_wrapper(INSERT_INCOMING_PART_BATCH, json=incoming_data, headers=headers)
#     incoming_response_json = incoming_response.json()
#     save_data = incoming_response_json.get("save_data")
#     if save_data is None:
#         raise HTTPException(status_code=500, detail=str(incoming_response_json))

#     save_data = [{
#         "data_name": "scan_items",
#         "data_value": save_data.get("scan_items", [])
#     }]
#     check_data = {
#         "scan_item": json_body.scan_item,
#         "data_name": 'J69_ADAPT_PCBA',
#         "device_name": json_body.device_name,
#         "station_name": json_body.station_name,
#         "save_data": save_data
#     }
#     check_route_response = mes_api_call_wrapper(CHECK_ROUTE_BATCH, json=check_data, headers=headers)
#     check_route_response_json = check_route_response.json()
#     if not check_route_response_json.get("success", False):
#         raise HTTPException(status_code=check_route_response.status_code, detail=str(check_route_response.json()))

#     data_version_url = f"{GET_VERSION}?scan_item={json_body.scan_item}"
#     data_version_response = mes_api_call_wrapper(data_version_url, is_get=True)

#     if data_version_response.status_code != 200:
#         raise HTTPException(status_code=data_version_response.status_code, detail=str(data_version_response.json()))

#     work_order_no = data_version_response.json().get("work_order_no")
#     test_data = {
#         "key_item": json_body.key_item,
#         "device_name": json_body.device_name,
#         "station_name": json_body.station_name,
#         "is_pass": json_body.is_pass,
#         "log_path": json_body.log_path,
#         "work_order_no": work_order_no,
#         "scan_item": json_body.scan_item,
#         "save_data": save_data,
#         "error_code": '99999',
#     }

#     test_result_response = mes_api_call_wrapper(INSERT_TEST_RESULT_BATCH, json=test_data, headers=headers)
#     if test_result_response.status_code != 200:
#         raise HTTPException(status_code=test_result_response.status_code, detail=str(test_result_response.json()))

#     return JSONResponse(
#         status_code=200,
#         content={
#             "status": "success",
#             "message": "Data successfully added to API!",
#             "data_incoming": incoming_response_json,
#             "data_check": check_route_response_json,
#             "data_result": test_result_response.json()
#         }
#     )