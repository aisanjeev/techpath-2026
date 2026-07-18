"""FastAPI application entry point."""
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.db.session import init_db
from app.middleware.error_handlers import setup_exception_handlers
from app.middleware.logging import LoggingMiddleware
from app.services.secrets_loader import load_secrets_from_keyvault, runtime_secrets


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Database: {'SQLite' if settings.is_sqlite else 'MySQL'}")

    # Load secrets from Azure Key Vault
    if settings.has_keyvault_config:
        logger.info("Loading secrets from Azure Key Vault...")
        secrets_result = await load_secrets_from_keyvault(update_db=True)
        loaded = sum(1 for v in secrets_result.values() if v)
        logger.info(f"Loaded {loaded}/{len(secrets_result)} secrets from Key Vault")
    else:
        logger.info("Key Vault not configured, using environment variables")

    # Determine storage type (Key Vault value takes precedence)
    storage_type = runtime_secrets.get("STORAGE_TYPE") or settings.STORAGE_TYPE
    logger.info(f"Storage: {storage_type}")

    # Initialize database
    await init_db()

    # One poll loop per worker process — see app/services/classroom/bus.py for why an
    # in-memory broadcaster alone isn't safe under --workers 2.
    from app.services.classroom.bus import start_poller

    start_poller()

    # Ensure upload directory exists for local storage and mount it
    if storage_type.lower() == "local":
        upload_path = Path(settings.LOCAL_UPLOAD_PATH)
        upload_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Local upload path: {upload_path.absolute()}")

        # Mount static files for uploads
        app.mount("/uploads", StaticFiles(directory=str(upload_path)), name="uploads")
        logger.info("Mounted /uploads for serving uploaded files")

    yield

    # Shutdown
    logger.info("Shutting down application...")

    from app.services.classroom.bus import stop_poller

    await stop_poller()

    # Release the outbound HTTP pool (roster API) rather than leaking sockets on reload.
    try:
        from app.services.roster.factory import get_roster_provider, reset_roster_provider

        await get_roster_provider().aclose()
        reset_roster_provider()
    except Exception as exc:  # noqa: BLE001 — shutdown must not raise
        logger.warning(f"Error closing roster provider: {exc}")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="API for TechPath Professional Services - AI-Powered IT Solutions",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
)

# CORS middleware — origins controlled via CORS_ORIGINS env var
# Expose X-Total-Count so admin/frontend can read pagination total
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],
)

# Logging middleware
app.add_middleware(LoggingMiddleware)

# Exception handlers
setup_exception_handlers(app)

# Include API router
app.include_router(v1_router, prefix="/api/v1")


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "database": "sqlite" if settings.is_sqlite else "mysql",
        "storage": settings.STORAGE_TYPE,
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else "Disabled in production",
        "health": "/health",
        "api": "/api/v1",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )

