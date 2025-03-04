from pydantic import BaseModel

class CheckRouteRequest(BaseModel):
    key_item: str
    device_name: str
    station_name: str
    is_pass: bool

class InsertSolderRequest(BaseModel):
    scan_item: str
    qty_per_batch: int
    device_name: str
    station_name: str
    key_item: str
    is_pass: bool
    log_path: str
    error_code: str