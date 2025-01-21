from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
import time


REQUEST_COUNT = Counter("app_requests_total", "Total number of requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Request latency", ["endpoint"])


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
        response = await call_next(request)
        request_latency = time.time() - start_time
        REQUEST_LATENCY.labels(endpoint=request.url.path).observe(request_latency)
        return response


async def metrics(request: Request):
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
