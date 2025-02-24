IS_LIVE = False

if IS_LIVE:
    LOGIN = "http://nusames.desay.satnusa.com:30401/sfis/login/"
    INSERT_RESULT = "http://nusames.desay.satnusa.com:30401/sfis/test_result/"
    INSERT_CHECK = "http://nusames.desay.satnusa.com:30401/sfis/check_route/"

    USERNAME = '11'
    PASSWORD = '11'

else:
    LOGIN = "http://nusames.desay.satnusa.com:32401/sfis/login/"
    INSERT_RESULT = "http://nusames.desay.satnusa.com:32401/sfis/test_result/"
    INSERT_CHECK = "http://nusames.desay.satnusa.com:32401/sfis/check_route/"

    USERNAME = 'test'
    PASSWORD = '11'
