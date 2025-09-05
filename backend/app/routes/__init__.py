# Legacy routes - will be replaced by new API structure
from fastapi import APIRouter
from .arkhamdb_routes import router as arkhamdb_router
from .app_route import router as app_router  
from .gpt_routes import router as gpt_router

# New API structure
from app.api.v1.api import api_router

# Create main router that includes both old and new
router = APIRouter()

# Include new API structure (recommended)
router.include_router(api_router, prefix="/v1")

# Include legacy routes (for backwards compatibility) 
router.include_router(arkhamdb_router, prefix="/legacy")
router.include_router(app_router, prefix="/legacy")
router.include_router(gpt_router, prefix="/legacy")
