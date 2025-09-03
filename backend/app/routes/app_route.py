from fastapi import APIRouter, Body, Depends, Response
from app.controllers.app_controller import AppController
from app.database import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.cache_service import cache_service
from app.core.config import settings
from typing import Optional


router = APIRouter(prefix="/app", tags=["app"])


@router.post("/fetch_cards/")
async def fetch_cards(encounter: int = 1, db: AsyncSession = Depends(get_async_db)):
    controller = AppController(db=db)
    return await controller.fetch_cards(encounter=encounter)


@router.get("/card/{card_code}/")
async def get_card(card_code: str, response: Response, db: AsyncSession = Depends(get_async_db)):
    """Get card with API-level caching headers"""
    controller = AppController(db=db)
    
    # Set cache headers for client-side caching
    response.headers["Cache-Control"] = f"public, max-age={settings.CACHE_TTL_CARDS}"
    response.headers["ETag"] = f'"{card_code}"'
    
    return await controller.get_card(card_code)


@router.get("/get_taboos/")
async def get_taboos(response: Response, db: AsyncSession = Depends(get_async_db)):
    """Get taboos with caching"""
    # Check cache first using generic method
    cached_taboos = await cache_service.get_with_key("taboos", "all")
    
    if cached_taboos:
        response.headers["Cache-Control"] = f"public, max-age={settings.CACHE_TTL_DEFAULT}"
        response.headers["X-Cache"] = "HIT"
        return cached_taboos
    
    # Get from controller if not cached
    controller = AppController(db=db)
    taboos = await controller.get_taboos()
    
    # Cache the result using generic method
    await cache_service.set_with_key("taboos", "all", taboos, ttl=settings.CACHE_TTL_DEFAULT)
    
    response.headers["Cache-Control"] = f"public, max-age={settings.CACHE_TTL_DEFAULT}"
    response.headers["X-Cache"] = "MISS"
    
    return taboos


@router.get("/cards/encounter/{encounter}")
async def get_cards_by_encounter(encounter: int, response: Response, limit: int = 100, db: AsyncSession = Depends(get_async_db)):
    """Get cards by encounter with caching"""
    controller = AppController(db=db)
    cards = await controller.get_cards_by_encounter(encounter, limit)
    
    response.headers["Cache-Control"] = f"public, max-age={settings.CACHE_TTL_CARDS}"
    response.headers["X-Cache"] = "PROCESSED"
    
    return {"cards": [card.model_dump() for card in cards], "total": len(cards)}

@router.get("/cards/search")
async def search_cards(q: str, page: int = 1, limit: int = 20, db: AsyncSession = Depends(get_async_db)):
    """Search cards with caching via service layer"""
    controller = AppController(db=db)
    results = await controller.search_cards(q, page, limit)
    return results

@router.get("/repositories/card")
async def access_card_repository(db: AsyncSession = Depends(get_async_db)):
    """Example of direct repository access via service layer"""
    controller = AppController(db=db)
    card_repo = await controller.get_card_repository()
    
    # Example: Get cards with complex filtering directly via repository
    cards = await card_repo.get_all(
        filter_by={"filter_by[encounter][equals]": 1},
        items_per_page=5,
        select_list=["traits"]
    )
    
    return {
        "message": "Direct repository access example",
        "cards_found": len(cards),
        "repository_type": type(card_repo).__name__
    }

@router.post("/sync/arkhamdb")
async def sync_with_arkhamdb(db: AsyncSession = Depends(get_async_db)):
    """Service-to-service communication example"""
    controller = AppController(db=db)
    result = await controller.sync_with_arkhamdb()
    return result

@router.get("/card/{card_code}/external")
async def get_card_with_external_data(card_code: str, db: AsyncSession = Depends(get_async_db)):
    """Compare local vs external data via service coordination"""
    controller = AppController(db=db)
    result = await controller.get_card_with_external_data(card_code)
    return result

@router.get("/analysis/popularity/{encounter}")
async def analyze_card_popularity(encounter: int, db: AsyncSession = Depends(get_async_db)):
    """Complex business logic using multiple services"""
    controller = AppController(db=db)
    result = await controller.analyze_card_popularity(encounter)
    return result
