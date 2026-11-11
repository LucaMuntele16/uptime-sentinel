from app.checker.classify import classify
    
def test_200_up():
    assert classify(200,120,1000) == "UP"    
def test_500():
    assert classify(500,120,1000) == "DEGRADED"
def test_none():
    assert classify(None,120,1000) == "DOWN"    
def test_latency_above():
    assert classify(200, 1500, 1000) == "DEGRADED"
def test_latency_treshold():
    assert classify(200,1000,1000) == "UP"    
def test_404():
    assert classify(404,120,1000) == "404"        