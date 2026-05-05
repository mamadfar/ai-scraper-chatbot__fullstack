
"""
Global error handler
"""

from doctest import debug
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

async def pydantic_validation_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """ Handles Pydantic validation errors (bad request body) """

    #* exc.errors() returns a list of validation failures
    errors = [
        {
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation failed",
            "status_code": 422,
            "errors": errors,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )

async def unhadled_exception_handler( request: Request, exc: Exception ) -> JSONResponse:
    """ Catches any exception we didn't handle explicitly - maps to HTTP 500 """

    logger.exception("Unhandled exception", exc_info=exc)

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "status_code": 500,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            # Never expose stack traces in production
            **({"debug": str(exc)} if settings.debug else {}) # This is a comprehension to add debug only in development mode
        }
    )