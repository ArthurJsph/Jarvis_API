import time
import os
from typing import Callable
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
RATE_LIMIT_PERIOD = int(os.getenv("RATE_LIMIT_PERIOD", "60"))  # seconds

# Simple in-memory token-bucket per api_key (sufficient for single-user / small deployment)
_buckets = {}


def _allow_request(key: str) -> bool:
    now = time.time()
    bucket = _buckets.get(key)
    if bucket is None:
        # tokens, last_refill
        _buckets[key] = [RATE_LIMIT_REQUESTS, now]
        return True

    tokens, last = bucket
    # refill proportionally
    elapsed = now - last
    # calculate fractional refill
    refill_tokens = (elapsed / RATE_LIMIT_PERIOD) * RATE_LIMIT_REQUESTS
    if refill_tokens >= 1:
        tokens = min(RATE_LIMIT_REQUESTS, int(tokens + refill_tokens))
        last = now

    if tokens <= 0:
        _buckets[key] = [tokens, last]
        return False

    tokens -= 1
    _buckets[key] = [tokens, last]
    return True


class APIKeyAndRateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        # Allow unauthenticated access to UI and static assets so users can load the page
        # without an API key. Only protect API endpoints.
        path = request.url.path or ""
        # Public paths that should not require API key (GET only)
        public_get_paths = ("/ui", "/", "/favicon.ico", "/openapi.json", "/docs", "/redoc")
        # Allow common static/ui routes and well-known probes (browser devtools), so the UI can load
        if request.method == "GET" and (path.startswith("/static") or path in public_get_paths or path.startswith("/.well-known")):
            return await call_next(request)

        # Allow CORS preflight and other safe methods through
        if request.method == "OPTIONS":
            return await call_next(request)

        # check api key header for protected endpoints
        key = request.headers.get("x-api-key") or request.query_params.get("api_key")
        if API_KEY is None:
            # no API key configured -> server misconfiguration
            raise HTTPException(status_code=500, detail="Server misconfiguration: API_KEY not set in environment")

        if key != API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API key")

        # rate limit per key
        if not _allow_request(key):
            raise HTTPException(status_code=429, detail="Too many requests")

        response = await call_next(request)
        return response
