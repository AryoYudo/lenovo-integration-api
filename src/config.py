IS_LIVE = False
BASE_URL = "http://nusames.lenovo.satnusa.com"

if IS_LIVE:
    PORT = "30401"
    USERNAME = '11'
    PASSWORD = '11'
else:
    PORT = "32401"
    USERNAME = 'test'
    PASSWORD = '11'

LOGIN = f"{BASE_URL}:{PORT}/sfis/login/"
INSERT_RESULT = f"{BASE_URL}:{PORT}/sfis/test_result/"
INSERT_CHECK = f"{BASE_URL}:{PORT}/sfis/check_route/"
