"""
Route definitions for the health module
"""
from datetime import datetime, timezone
from fastapi import APIRouter

from app.core.config import settings
from app.modules.health.schemas import HealthResponse

# APIRouter is like Express's Router()
# prefix="/health" means all routes here start with /health
# tags=["Health"] groups them in Swagger UI
router = APIRouter(prefix="/health", tags=["Health"])


# @router.get("") defines a GET endpoint at /health
# response_model tells FastAPI what shape the response will be -
# it auto-validates AND auto-generates Swagger docs
@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    Used by Docker, load balancers, and monitoring tools
    """
    return HealthResponse(
        status="ok",
        version=settings.app_version,
        timestamp=datetime.now(timezone.utc)
    )