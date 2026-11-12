import requests
from unittest.mock import patch, MagicMock
from app.checker.checker import check_site
from app.checker.classify import classify

#Test 1: I verify that a succesful 200 Ok response classifies the site as UP
def test_site_ok_is_up():
    response_false = MagicMock(status_code=200) #Create a mock response object with status_code 200
    with patch("app.checker.checker.requests.get", return_value=response_false): #Patch requests.get so it return our mock response instead of hitting the internet
        result = check_site("test","https://example.test",5,1000)
    assert result["http_code"] == 200
    assert result["status"] == "UP"
    
#Test 2: Verify that a network timeout correctly classifies the site as DOWN
def test_timeout_is_down():
    with patch("app.checker.checker.requests.get", side_effect = requests.exceptions.Timeout()): #Patch requests.get to raise a timeout exception
        result = check_site("test", "https://example.test",5,1000)
    assert result["http_code"] is None
    assert result["status"] == "DOWN"       

#Test 3: Verify that a connection error classifies the site as DOWN, the http_code is None and that the error message is saved
def test_connection_error():
    with patch("app.checker.checker.requests.get", side_effect=requests.exceptions.ConnectionError()):
        result = check_site("test", "https://example.test",5,100)
    assert result["http_code"] is None
    assert result["status"] == "DOWN"    
    assert result["error"] is not None