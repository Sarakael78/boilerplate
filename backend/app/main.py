"""
Main application entry point for the FastAPI backend.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.users import router as users_router
from .db.database import engine
from .models import user

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
user.Base.metadata.create_all(bind=engine)

# Create the FastAPI app instance
app = FastAPI(
    title=settings.APP_NAME,
    description="A modern full-stack application backend",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(users_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """
    Simple health check endpoint to confirm the API is running.
    """
    return {"status": "ok", "service": settings.APP_NAME}


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    """
    Root endpoint with API information.
    """
    return {
        "message": "Welcome to the API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }
