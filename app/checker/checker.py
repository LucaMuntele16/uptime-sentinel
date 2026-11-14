import time
import requests
from app.checker.classify import classify

def check_site(name, url, timeout_s, threshold_ms):
    start = time.perf_counter()
    try:
        response = requests.get(url, timeout=timeout_s)
        latency_ms = (time.perf_counter() - start) * 1000
        http_code = response.status_code
        error = None
    except requests.exceptions.RequestException as exc:
        latency_ms = (time.perf_counter() - start) * 1000
        http_code = None
        error = str(exc)
    status = classify(http_code, latency_ms, threshold_ms)
    return{
        "name":name,
        "url":url,
        "http_code":http_code,
        "latency_ms":round(latency_ms, 1),
        "error": error,
        "status":status
    }        
def check_all(sites, threshold_ms, timeout_s=5):
    results = []
    for site in sites:
        result = check_site(site["name"], site["url"], timeout_s, threshold_ms)
        results.append(result)
    return results    