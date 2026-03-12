from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.core.config import settings
from app.core.redis_client import redis_client
from app.adapters import initialize_card_adapters
import uvicorn
import logging

logger = logging.getLogger(__name__)

# Try to import FastAPICache, but make it optional


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    # Startup
    try:
        # Initialize card adapters (registers adapters with domain registry)
        initialize_card_adapters()
        logger.info("Card adapters initialized")
        
        await redis_client.connect()
        if redis_client.is_connected:

            logger.info("FastAPI Cache initialized with Redis")
        elif redis_client.is_connected:
            logger.info("Redis connected but FastAPICache not available")
        else:
            logger.info("FastAPI Cache not initialized - Redis not available")
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

    yield

    # Shutdown
    try:
        await redis_client.disconnect()
        logger.info("Application shutdown completed successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


app = FastAPI(
    title="Arkham Analysis API",
    description="API for analyzing Arkham Horror cards",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI at /docs
    redoc_url="/redoc",  # ReDoc at /redoc
    lifespan=lifespan,
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI application"}


@app.get("/health")
async def health_check():
    """Health check endpoint with Redis status"""
    try:
        # Check Redis connection
        redis_stats = await redis_client.get_stats()
        return {"status": "healthy", "redis": {"connected": True, "stats": redis_stats}}
    except Exception as e:
        return {"status": "unhealthy", "redis": {"connected": False, "error": str(e)}}


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        reload_dirs=["app"],
    )
