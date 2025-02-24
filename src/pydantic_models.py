from pydantic import BaseModel

class CheckRouteRequest(BaseModel):
    key_item: str
    data_name: str
    device_name: str
    station_name: str
    is_pass: bool
    error_code: str
    log_path: str
    log_data: str

class InsertSolderRequest(BaseModel):
    scan_item: str
    qty_per_batch: int
    device_name: str
    station_name: str
    key_item: str
    is_pass: bool
    log_path: str   