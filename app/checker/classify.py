def classify(http_code, latency_ms,threshold_ms):
    if http_code is None:
        return "DOWN"
    if http_code >= 500:
        return "DEGRADED"
    if http_code == 404:
        return "404"
    if latency_ms > threshold_ms:
        return "DEGRADED"
    return "UP"