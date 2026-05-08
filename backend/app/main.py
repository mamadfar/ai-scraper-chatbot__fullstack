
import sys
from contextlib import asynccontextmanager

from loguru import logger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.modules.health.router import router as health_router
from app.core.config import settings
from app.core.exceptions import AppException
from app.middleware.error_handler import (app_exception_handler, pydantic_validation_handler, unhadled_exception_handler)
from app.middleware.rate_limiter import limiter, rate_limit_exceeded_handler

#* [LOGURU] Remove all default handlers, add a clean one
logger.remove()
logger.add(
    sys.stdout, # 
    level="DEBUG" if settings.debug else "INFO",
    # structured format — easy to parse in Grafana later
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{line} | {message}",
    colorize=True
)

#* [LOGURU] Also, write errors to a file
logger.add(
    "logs/error.log",
    level="ERROR",
    rotation="10 MB", # new file when it hits 10MB
    retention="30 days", # delete logs older than 30 days
    compression="zip", # compress logs
)

# lifespan is FastAPI's way to run code on startup and shutdown.
# In Express we'd do: app.listen(PORT, () => console.log('Running'))
# and process.on('SIGTERM', () => server.close())
#
# asynccontextmanager turns this into an async context manager.
# The code BEFORE yield runs on startup.
# The code AFTER yield runs on shutdown.

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug}")
    # DB + Other services startup
    yield
    # Shutdown
    logger.info(f"Shutting down...")


#* [FASTAPI] Create the FastAPI app - like `const app = express()`
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="RAG-powered chatbot microservice",
    # Swagger UI is at /docs
    docs_url="/_/docs" if settings.debug else None,
    redoc_url="/_/redoc" if settings.debug else None, # Redoc is an alternative to Swagger UI
    lifespan=lifespan
)

# Add rate limiter to the app state
app.state.limiter = limiter

#? Middleware ----------------------------------------------------------------
# CORS middleware - smae concept as cors() in Express
# In production, we should replace "*" with our actual frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#* [SLOWAPI] Register the rate limit middleware
app.add_middleware(SlowAPIMiddleware)

#? Exception handlers ------------------------------------------------------------
# Register global exception handlers - Order matters!
# Most specific first, most general last
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(ValidationError, pydantic_validation_handler)
app.add_exception_handler(Exception, unhadled_exception_handler)
#* [SLOWAPI] Register the rate limit error handler
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

#? Routers ----------------------------------------------------------------------
# Register routers - like app.use('/health, healthRouter) in Express
# prefix="/api/v1" prepends to all routes, so health becomes /api/v1/health
app.include_router(health_router, prefix=settings.api_prefix)

# The limit string format is: "number/period"
# periods: second, minute, hour, day
# Examples: "10/minute", "100/hour", "5/second"

# @router.get("/")
# @limiter.limit("10/minute")  # ← add this decorator
# async def some_route(request: Request):  # ← Request param required by slowapi

# Root endpoint - basic health check
@app.get("/", include_in_schema=False) # Exclude from Swagger UI
async def root() -> dict:
    return {"message": f"{settings.app_name} with V{settings.app_version} is running"}