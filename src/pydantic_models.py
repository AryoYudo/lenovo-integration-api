from pydantic import BaseModel

class CheckRouteRequest(BaseModel):
    key_item: str
    device_name: str
    station_name: str
    is_pass: bool
