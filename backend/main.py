"""
Entry point for the FastAPI application.
This module exposes the app for uvicorn to run.
"""

from src.main import app

__all__ = ["app"]


if __name__ == "__main__":
    import uvicorn
    from src.config import settings

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
