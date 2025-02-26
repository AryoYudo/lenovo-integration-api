IS_LIVE = False
# BASE_URL = "http://nusames.lenovo.satnusa.com"                    #Api Mes
BASE_URL = "https://67bd2af6321b883e790b6d40.mockapi.io/sfis/"      #Api buat testing

if IS_LIVE:
    PORT = "30401"
    USERNAME = '11'
    PASSWORD = '11'
else:
    PORT = "32401"
    USERNAME = 'test'
    PASSWORD = '11'

# Api Mes 
# LOGIN = f"{BASE_URL}:{PORT}/sfis/login/"
# INSERT_RESULT = f"{BASE_URL}:{PORT}/sfis/test_result/"
# INSERT_CHECK = f"{BASE_URL}:{PORT}/sfis/check_route/"
GET_VERSION = "http://nusames.desay.satnusa.com:32401/sfis/get_version2/"

# Api Testing
LOGIN = f"{BASE_URL}login/"
INSERT_RESULT = f"{BASE_URL}test_results"
INSERT_CHECK = f"{BASE_URL}check_route"
