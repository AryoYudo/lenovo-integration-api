import secrets

from fastapi import Request, APIRouter, HTTPException
from fastapi.responses import JSONResponse

from src.config import INSERT_RESULT, INSERT_CHECK
from src.helpers import get_token, mes_api_call_wrapper
from src.pydantic_models import CheckRouteRequest

router = APIRouter()
secret_key = secrets.token_hex(32)

@router.post("/insert_check")
async def insert_check(request: Request, json_body: CheckRouteRequest):
    token = get_token(json_body)
    token_auth = 'token ' + token

    check_route = {
        "scan_item": json_body.key_item,
        "device_name": json_body.device_name,
        "station_name": json_body.station_name
    }
    checkroute_resp = mes_api_call_wrapper(INSERT_CHECK, json=check_route, headers={"Authorization": token_auth, "Content-Type": "application/json"})

    if checkroute_resp.status_code not in {200, 201}:
        raise HTTPException(status_code=checkroute_resp.status_code, detail=str(checkroute_resp.json()))

    test_result = {
        "key_item": json_body.key_item,
        "station_name": json_body.station_name,
        "device_name": json_body.device_name,
        "is_pass": json_body.is_pass
    }

    insert_resp = mes_api_call_wrapper(INSERT_RESULT, json=test_result, headers={"Authorization": token_auth, "Content-Type": "application/json"})

    if insert_resp.status_code not in {200, 201}:
        raise HTTPException(status_code=insert_resp.status_code, detail=str(insert_resp.json()))

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "message": "Data successfully added to API!",
            "data": insert_resp.json()
        }
    )
