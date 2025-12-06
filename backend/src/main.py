"""
Main FastAPI application for RAG Chatbot Backend.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routes import chat_router, content_router, documents_router, health_router


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    logger.info("Starting RAG Chatbot API...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Gemini Model: {settings.gemini_model}")
    logger.info(f"Qdrant Mode: {settings.qdrant_mode}")

    yield

    # Shutdown
    logger.info("Shutting down RAG Chatbot API...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description=settings.app_description,
    debug=settings.debug,
    lifespan=lifespan
)


# Configure CORS
if settings.cors_enabled:
    logger.info(f"CORS enabled for origins: {settings.cors_origins_list}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Include routers
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(content_router)
app.include_router(documents_router)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API information.
    """
    return {
        "name": settings.app_title,
        "version": settings.app_version,
        "description": settings.app_description,
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
