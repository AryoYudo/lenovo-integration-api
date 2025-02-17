from config import IS_LIVE

if not IS_LIVE:
    LOGIN = "http://nusames.desay.satnusa.com:32401/sfis/login/"  
    INSERT_INCOMING_PART_BATCH = "http://nusames.desay.satnusa.com:32302/incoming-parts/get_sibling_incoming_part/"  
    CHECK_ROUTE_BATCH = "http://nusames.desay.satnusa.com:32401/sfis/check_route_batch/"  
    INSERT_TEST_RESULT_BATCH = "http://nusames.desay.satnusa.com:32401/sfis/test_result_batch/"  
    GET_VERSION = "http://nusames.desay.satnusa.com:32401/sfis/get_version2/" 

    INSERT_RESULT_PCB = "http://nusames.desay.satnusa.com:32401/sfis/test_result/"  
    INSERT_CHECK_PCB = "http://nusames.desay.satnusa.com:32401/sfis/check_route/"     
    
else:
    LOGIN = "http://nusames.desay.satnusa.com:30401/sfis/login/"  
    INSERT_INCOMING_PART_BATCH = "http://nusames.desay.satnusa.com:30302/incoming-parts/get_sibling_incoming_part/"  
    CHECK_ROUTE_BATCH = "http://nusames.desay.satnusa.com:30401/sfis/check_route_batch/"  
    INSERT_TEST_RESULT_BATCH = "http://nusames.desay.satnusa.com:30401/sfis/test_result_batch/" 
    GET_VERSION = "http://nusames.desay.satnusa.com:32401/sfis/get_version2/"     

    INSERT_RESULT_PCB = "http://nusames.desay.satnusa.com:30401/sfis/test_result/"  
    INSERT_CHECK_PCB = "http://nusames.desay.satnusa.com:30401/sfis/check_route/" 