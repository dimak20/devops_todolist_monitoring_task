import time
from prometheus_client import Counter, Summary

REQUEST_COUNT = Counter(
    "django_http_requests_total",
    "Total HTTP Requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Summary(
    "django_http_requests_latency_seconds",
    "HTTP Requests Creation Time"
)

class PrometheusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        REQUEST_COUNT.labels(method=request.method, endpoint=request.path).inc()

        start_time = time.time()
        response = self.get_response(request)
        
        resp_time = time.time() - start_time
        REQUEST_LATENCY.observe(resp_time)
        
        return response