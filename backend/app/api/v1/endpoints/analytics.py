from fastapi import APIRouter, Depends
from typing import Dict, Any, List
from app.api.deps import get_app_service, get_cache_service
from app.services.app_service import AppService
from app.services.cache_service import CacheService

router = APIRouter()


@router.get("/popularity/{encounter}")
async def analyze_card_popularity(
    encounter: int, app_service: AppService = Depends(get_app_service)
):
    """Analyze card popularity for an encounter"""
    analysis = await app_service.analyze_card_popularity(encounter)
    return analysis


@router.get("/repositories/card")
async def repository_access_example(app_service: AppService = Depends(get_app_service)):
    """Example of direct repository access for complex queries"""
    card_repo = await app_service.get_card_repository()

    # Complex query example
    cards = await card_repo.get_all(
        filter_by={"filter_by[encounter][equals]": 1},
        items_per_page=5,
        include=["traits"],
    )

    return {
        "message": "Direct repository access example",
        "cards_found": len(cards),
        "repository_type": type(card_repo).__name__,
        "sample_cards": [card.name for card in cards[:3]] if cards else [],
    }


@router.get("/cache/stats")
async def get_cache_stats(cache_service: CacheService = Depends(get_cache_service)):
    """Get cache statistics and health"""
    from app.core.redis_client import redis_client

    stats = await redis_client.get_stats()

    return {
        "redis_connected": redis_client.is_connected,
        "redis_stats": stats,
        "cache_service_type": type(cache_service).__name__,
    }


@router.delete("/cache/clear")
async def clear_cache(
    pattern: str = "*", cache_service: CacheService = Depends(get_cache_service)
):
    """Clear cache entries by pattern"""
    if pattern == "*":
        # Clear all arkham-related cache
        deleted = await cache_service.invalidate_by_tags(
            "card", "cards", "traits", "taboos", "arkhamdb"
        )
    else:
        # Clear specific pattern
        deleted = await cache_service.invalidate_by_pattern("arkham", pattern)

    return {
        "message": f"Cache cleared for pattern: {pattern}",
        "entries_deleted": deleted,
    }
