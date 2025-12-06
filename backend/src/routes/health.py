"""
Health check routes for API monitoring.
"""

import logging
from fastapi import APIRouter

from ..models import HealthResponse
from ..services import qdrant_service
from ..config import settings


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "/",
    response_model=HealthResponse,
    summary="Health check",
    description="Check the health status of the API and its dependencies."
)
async def health_check() -> HealthResponse:
    """
    Perform a health check on the API and its dependencies.

    Returns information about:
    - API status
    - API version
    - Qdrant connection status
    - Collection existence
    """
    try:
        # Check Qdrant health
        qdrant_health = qdrant_service.health_check()

        return HealthResponse(
            status="healthy",
            version=settings.app_version,
            qdrant_connected=qdrant_health.get("connected", False),
            collection_exists=qdrant_health.get("collection_exists", False)
        )

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            version=settings.app_version,
            qdrant_connected=False,
            collection_exists=False
        )
