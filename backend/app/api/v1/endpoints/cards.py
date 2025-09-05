from fastapi import APIRouter, Depends, HTTPException, Response, status, Body
from typing import List
from app.schemas.card_schema import CardSchema
from app.services.app_service import AppService

# Import shared utilities from endpoints __init__.py
from . import (
    get_validated_app_service,
    get_card_code_param,
    get_encounter_param,
    get_pagination_params,
    get_search_params,
    get_sorting_params,
    ArkhamApiResponse,
    CardSummary,
    PaginatedCardResponse,
    ScoringResult,
    CARD_NOT_FOUND,
    INVALID_CARD_CODE,
    ARKHAM_HEADERS,
    CACHE_TTL_MEDIUM,
)

router = APIRouter(prefix="/cards", tags=["cards"])


@router.post("/fetch_cards", response_model=List[CardSchema])
async def fetch_cards(
    encounter: int,
    app_service: AppService = Depends(get_validated_app_service),
):
    """Fetch and return cards from an encounter set"""
    try:
        # First try to sync the cards from ArkhamDB
        try:
            await app_service.fetch_cards(encounter)
        except Exception as sync_error:
            # If ArkhamDB sync fails, log it but continue
            import logging

            logger = logging.getLogger(__name__)
            logger.warning(
                f"ArkhamDB sync failed for encounter {encounter}: {str(sync_error)}"
            )
        return []
        # Then get the cards from the database (either newly synced or existing)
        # cards = await app_service.get_cards_by_encounter(encounter)
        # return cards if cards is not None else []
    except Exception as e:
        # Log the actual error for debugging
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"as {encounter}: {str(e)}")

        # Return empty list instead of raising exception to avoid 500 error
        return []


@router.get("/{card_code}", response_model=CardSchema)
async def get_card(
    response: Response,
    card_code: str = Depends(get_card_code_param),  # ✅ Shared validator
    app_service=Depends(get_validated_app_service),  # ✅ Shared dependency
):
    """Get a single Arkham Horror card by code"""
    try:
        card = await app_service.get_card(card_code)

        # Set Arkham-specific headers
        response.headers.update(ARKHAM_HEADERS)
        response.headers["Cache-Control"] = f"public, max-age={CACHE_TTL_MEDIUM}"
        response.headers["ETag"] = f'"{card_code}"'

        return card
    except Exception:
        raise CARD_NOT_FOUND  # ✅ Shared exception


@router.get("/encounter/{encounter}/cards", response_model=PaginatedCardResponse)
async def get_cards_by_encounter(
    response: Response,
    encounter: int = Depends(get_encounter_param),  # ✅ Shared validator
    pagination=Depends(get_pagination_params),  # ✅ Shared pagination,
    app_service=Depends(get_validated_app_service),
):
    """Get cards from a specific encounter set"""
    cards = await app_service.get_cards_by_encounter(
        encounter, limit=pagination["limit"]
    )

    # Convert to summary format
    card_summaries = [
        CardSummary(
            code=card.code,
            name=card.name,
            faction_code=card.faction_code,
            type_code=card.type_code,
            xp=card.xp,
            cost=card.cost,
        )
        for card in cards
    ]

    response.headers.update(ARKHAM_HEADERS)
    response.headers["Cache-Control"] = f"public, max-age={CACHE_TTL_MEDIUM}"

    return PaginatedCardResponse(
        cards=card_summaries,
        pagination={
            "page": pagination["page"],
            "limit": pagination["limit"],
            "has_next": len(cards) >= pagination["limit"],
            "has_prev": pagination["page"] > 1,
        },
        filters={"encounter": encounter},
        total_results=len(cards),
    )


@router.get("/search", response_model=PaginatedCardResponse)
async def search_cards(
    response: Response,
    search_params=Depends(get_search_params),  # ✅ Advanced search params
    pagination=Depends(get_pagination_params),  # ✅ Shared pagination
    sorting=Depends(get_sorting_params),  # ✅ Shared sorting
    app_service=Depends(get_validated_app_service),
):
    """Advanced search for Arkham Horror cards"""
    results = await app_service.search_cards(
        search_params["query"], pagination["page"], pagination["limit"]
    )

    response.headers.update(ARKHAM_HEADERS)

    # This would be enhanced with your actual search results format
    return PaginatedCardResponse(
        cards=[],  # Your search results here
        pagination=pagination,
        filters=search_params,
        total_results=0,
    )


@router.get("/{card_code}/score", response_model=ScoringResult)
async def get_card_score(
    response: Response,
    card_code: str = Depends(get_card_code_param),
    app_service=Depends(get_validated_app_service),
):
    """Get calculated score for a card using scoring model"""
    try:
        # This would integrate with your scoring model
        score = await app_service.calculate_card_value(card_code)

        response.headers.update(ARKHAM_HEADERS)
        response.headers["Cache-Control"] = f"public, max-age={CACHE_TTL_MEDIUM}"

        return ScoringResult(
            card_code=card_code,
            score=score,
            algorithm="base_evaluator",
            factors={"base_score": score},  # Would be expanded with actual factors
        )
    except Exception:
        raise CARD_NOT_FOUND


@router.post("/bulk/score", response_model=List[ScoringResult])
async def bulk_score_cards(
    card_codes: List[str], app_service=Depends(get_validated_app_service)
):
    """Score multiple cards in bulk (uses shared validation)"""
    from . import validate_card_codes  # ✅ Shared validator

    validated_codes = validate_card_codes(card_codes)

    results = []
    for code in validated_codes:
        try:
            score = await app_service.calculate_card_value(code)
            results.append(
                ScoringResult(card_code=code, score=score, algorithm="base_evaluator")
            )
        except:
            # Skip cards that can't be scored
            continue

    return results
