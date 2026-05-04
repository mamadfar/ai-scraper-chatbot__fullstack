
"""
Global error handler
"""

import logging
from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.config import settings
from app.core.exceptions import AppException

#? logging is Python's built-in logger - like console.log() but structured
# In production we'd swap this for structlog or loguru
logger = logging.getLogger(__name__)

# This is a FastAPI exception handler — a function that catches
# a specific exception type and returns an HTTP response.
# In Express we'd do: app.use((err, req, res, next) => { ... })

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """ Handles all AppException subclasses (our custom errors) """

    logger.error("Application error", extra={
        "status_code": exc.status_code,
        "message": exc.message,
        "path": request.url.path
    })

    return JSONResponse(
        status_code = exc.status_code,
        content = {
            "detail": exc.message,
            "status_code": exc.status_code,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            #* Only show extra details in debug mode (development)
            **({"details": exc.details} if exc.details and settings.debug else {})
        }
    )