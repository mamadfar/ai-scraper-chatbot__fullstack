
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime, timezone

#? get_remote_address extracts the client's IP from the request
# This is the "key" slowapi uses to track request counts per client
# In TS (express-rate-limit): keyGenerator: (req) => req.ip
limiter = Limiter(key_func=get_remote_address)

async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """ Retkurns a clean JSON error when rate limit is hit instead of slowapi's default """

    return JSONResponse(
        status_code=429,
        content={
            "detail": f"Rate limit exceeded. Try again later after {exc.headers['Retry-After']} seconds",
            "status_code": 429,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )