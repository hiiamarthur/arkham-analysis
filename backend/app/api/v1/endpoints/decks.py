from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Any, List
from app.services.arkhamdb_service import ArkhamDBService
from app.services.deck_service import DeckService
from app.api.deps import get_arkhamdb_service, get_deck_service
from app.schemas.card_schema import DeckListSchema

router = APIRouter()


@router.get("/by_date/{date}")
async def get_decks_by_date(
    date: str, arkhamdb_service: ArkhamDBService = Depends(get_arkhamdb_service)
) -> List[DeckListSchema]:
    try:
        return await arkhamdb_service.fetch_decks_by_date(date)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get decks by date: {str(e)}"
        )


@router.get("/last_30_days")
async def get_decks_last_30_days(
    deck_service: DeckService = Depends(get_deck_service),
) -> Any:
    """Get all decks from the last 30 days"""
    return await deck_service.get_deck_summary(30)


@router.get("/last_n_days")
async def get_decks_last_n_days(
    days: int = Query(
        ..., ge=1, le=4000, description="Number of days to fetch (max ~11 years)"
    ),
    batch_size: int = Query(30, ge=1, le=100, description="Days per batch"),
    max_concurrent: int = Query(10, ge=1, le=50, description="Max concurrent requests"),
    use_cache: bool = Query(True, description="Use Redis caching"),
    deck_service: DeckService = Depends(get_deck_service),
) -> Any:
    """Get all decks from the last N days with batched processing and caching"""
    try:
        return await deck_service.get_deck_summary(
            days=days,
            batch_size=batch_size,
            max_concurrent=max_concurrent,
            use_cache=use_cache,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get decks for last {days} days: {str(e)}",
        )
