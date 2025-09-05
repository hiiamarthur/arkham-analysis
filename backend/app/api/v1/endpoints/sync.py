from fastapi import APIRouter, Depends, BackgroundTasks
from typing import Dict, Any
from app.api.deps import get_app_service, get_arkhamdb_service
from app.services.app_service import AppService
from app.services.arkhamdb_service import ArkhamDBService

router = APIRouter()


@router.post("/cards")
async def sync_cards(
    encounter: int = 0,
    background_tasks: BackgroundTasks = None,
    app_service: AppService = Depends(get_app_service)
):
    """Sync cards from ArkhamDB"""
    if background_tasks:
        # Run sync in background for large operations
        background_tasks.add_task(app_service.fetch_cards, encounter)
        return {
            "status": "started",
            "message": f"Card sync for encounter {encounter} started in background"
        }
    else:
        # Run sync synchronously for smaller operations
        await app_service.fetch_cards(encounter)
        return {
            "status": "completed",
            "message": f"Card sync for encounter {encounter} completed"
        }


@router.get("/taboos")
async def sync_taboos(
    app_service: AppService = Depends(get_app_service)
):
    """Sync taboo data from ArkhamDB"""
    taboos = await app_service.get_taboos()
    return {
        "status": "completed",
        "taboos_synced": len(taboos),
        "data": taboos
    }


@router.post("/arkhamdb/full")
async def full_arkhamdb_sync(
    app_service: AppService = Depends(get_app_service)
):
    """Complete sync with ArkhamDB - health check, cards, and taboos"""
    result = await app_service.sync_with_arkhamdb()
    return result


@router.get("/arkhamdb/health")
async def check_arkhamdb_health(
    arkhamdb_service: ArkhamDBService = Depends(get_arkhamdb_service)
):
    """Check ArkhamDB API health"""
    health = await arkhamdb_service.health_check()
    return health