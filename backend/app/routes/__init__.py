from flask import Blueprint
from .arkhamdb_routes import router as arkhamdb_router
from .app_route import router as app_router

from fastapi import APIRouter

router = APIRouter()
router.include_router(arkhamdb_router)
router.include_router(app_router)
