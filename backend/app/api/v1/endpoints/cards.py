from fastapi import APIRouter, Depends, HTTPException, Response, status, Body
from typing import List, Optional
from app.schemas.card_schema import CardSchema
from app.services.app_service import AppService
from app.api.deps import get_card_service
from app.services.card_service import CardService

# Import shared utilities from endpoints __init__.py
from . import (
    get_validated_app_service,
    get_card_code_param,
    get_investigator_code_param,
    get_encounter_param,
    get_pagination_params,
    get_search_params,
    get_sorting_params,
    CardSummary,
    PaginatedCardResponse,
    ScoringResult,
    CARD_NOT_FOUND,
    ARKHAM_HEADERS,
    CACHE_TTL_MEDIUM,
)

router = APIRouter()


@router.get("/metadata/traits", response_model=List[str])
async def get_all_traits(
    response: Response,
    card_service: CardService = Depends(get_card_service),
):
    """
    Get a list of all unique card traits in the database.
    Results are cached for performance.
    """
    try:
        traits = await card_service.get_all_traits()

        response.headers.update(ARKHAM_HEADERS)
        response.headers["Cache-Control"] = (
            "public, max-age=86400"  # Cache for 24 hours
        )

        return traits
    except Exception as e:
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"Error getting traits: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting traits: {str(e)}")


@router.get("/metadata/investigators", response_model=List[dict])
async def get_all_investigators(
    response: Response,
    card_service: CardService = Depends(get_card_service),
):
    """
    Get a list of all investigators with their codes and names.
    Results are cached for performance.
    """
    try:
        investigators = await card_service.get_all_investigators()

        response.headers.update(ARKHAM_HEADERS)
        response.headers["Cache-Control"] = (
            "public, max-age=86400"  # Cache for 24 hours
        )

        return investigators
    except Exception as e:
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"Error getting investigators: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error getting investigators: {str(e)}"
        )


@router.get("/metadata/encounter_sets", response_model=List[dict])
async def get_all_encounter_sets(
    response: Response,
    card_service: CardService = Depends(get_card_service),
):
    """
    Get a list of all unique encounter sets in the database.
    Returns list of {code, name} objects.
    Results are cached for performance.
    """
    try:
        encounter_sets = await card_service.get_all_encounter_sets()

        response.headers.update(ARKHAM_HEADERS)
        response.headers["Cache-Control"] = (
            "public, max-age=86400"  # Cache for 24 hours
        )

        return encounter_sets
    except Exception as e:
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"Error getting encounter sets: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error getting encounter sets: {str(e)}"
        )


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


@router.get("/search", response_model=PaginatedCardResponse)
async def search_cards(
    response: Response,
    # Text search
    q: Optional[str] = None,
    text: Optional[str] = None,
    flavor: Optional[str] = None,
    # Class/Faction
    faction: Optional[str] = None,
    # Card attributes
    card_type: Optional[str] = None,
    subtype: Optional[str] = None,
    traits: Optional[str] = None,
    slot: Optional[str] = None,
    pack_code: Optional[str] = None,
    illustrator: Optional[str] = None,
    # Boolean filters
    is_unique: Optional[bool] = None,
    permanent: Optional[bool] = None,
    exceptional: Optional[bool] = None,
    # Numeric filters
    min_xp: Optional[int] = None,
    max_xp: Optional[int] = None,
    min_cost: Optional[int] = None,
    max_cost: Optional[int] = None,
    min_skill_willpower: Optional[int] = None,
    max_skill_willpower: Optional[int] = None,
    min_skill_intellect: Optional[int] = None,
    max_skill_intellect: Optional[int] = None,
    min_skill_combat: Optional[int] = None,
    max_skill_combat: Optional[int] = None,
    min_skill_agility: Optional[int] = None,
    max_skill_agility: Optional[int] = None,
    min_health: Optional[int] = None,
    max_health: Optional[int] = None,
    min_sanity: Optional[int] = None,
    max_sanity: Optional[int] = None,
    pagination=Depends(get_pagination_params),
    card_service: CardService = Depends(get_card_service),
):
    """
    Advanced search for Arkham Horror cards with comprehensive filtering.

    Text Search:
    - q: Search in card name
    - text: Search in card text
    - flavor: Search in flavor text

    Card Attributes:
    - faction: guardian, seeker, rogue, mystic, survivor, neutral
    - card_type: asset, event, skill, investigator, etc.
    - subtype: Weakness, Basicweakness, etc.
    - traits: Filter by trait (e.g., "Weapon", "Spell")
    - slot: Hand, Ally, Arcane, etc.
    - pack_code: core, dwl, ptc, etc.
    - illustrator: Artist name

    Boolean Filters:
    - is_unique: true/false
    - permanent: true/false
    - exceptional: true/false

    Numeric Ranges:
    - cost, xp, health, sanity
    - skill_willpower, skill_intellect, skill_combat, skill_agility

    Pagination:
    - page, limit
    """
    try:
        # Get paginated results from service
        total_count, cards = await card_service.search_cards_paginated(
            query=q,
            text_search=text,
            flavor_search=flavor,
            faction=faction,
            card_type=card_type,
            subtype=subtype,
            traits=traits,
            slot=slot,
            pack_code=pack_code,
            illustrator=illustrator,
            is_unique=is_unique,
            permanent=permanent,
            exceptional=exceptional,
            min_xp=min_xp,
            max_xp=max_xp,
            min_cost=min_cost,
            max_cost=max_cost,
            min_skill_willpower=min_skill_willpower,
            max_skill_willpower=max_skill_willpower,
            min_skill_intellect=min_skill_intellect,
            max_skill_intellect=max_skill_intellect,
            min_skill_combat=min_skill_combat,
            max_skill_combat=max_skill_combat,
            min_skill_agility=min_skill_agility,
            max_skill_agility=max_skill_agility,
            min_health=min_health,
            max_health=max_health,
            min_sanity=min_sanity,
            max_sanity=max_sanity,
            page=pagination["page"],
            limit=pagination["limit"],
        )

        # Convert to summary format for better performance
        card_summaries = [
            CardSummary(
                code=card.code,
                name=card.name,
                faction_code=card.faction_code,
                type_code=card.type_code,
                xp=0,  # XP not available in CardSchema
                cost=card.cost,
                pack_code=card.pack_code,
                traits=[trait.name for trait in card.traits],
                illustrator=card.illustrator,
            )
            for card in cards
        ]

        response.headers.update(ARKHAM_HEADERS)
        response.headers["Cache-Control"] = f"public, max-age={CACHE_TTL_MEDIUM}"
        response.headers["X-Total-Count"] = str(total_count)

        return PaginatedCardResponse(
            cards=card_summaries,
            pagination={
                "page": pagination["page"],
                "limit": pagination["limit"],
                "has_next": pagination["page"] * pagination["limit"] < total_count,
                "has_prev": pagination["page"] > 1,
            },
            filters={
                "q": q,
                "faction": faction,
                "card_type": card_type,
                "min_xp": min_xp,
                "max_xp": max_xp,
                "min_cost": min_cost,
                "max_cost": max_cost,
                "pack_code": pack_code,
                "traits": traits,
            },
            total_results=total_count,
        )
    except Exception as e:
        import logging

        logger = logging.getLogger(__name__)
        logger.error(f"Error searching cards: {e}")
        raise HTTPException(status_code=500, detail=f"Error searching cards: {str(e)}")


@router.get("/{card_code}", response_model=CardSchema)
async def get_card(
    response: Response,
    card_code: str = Depends(get_card_code_param),  # ✅ Shared validator
    app_service=Depends(get_validated_app_service),  # ✅ Shared dependency
    card_service: CardService = Depends(get_card_service),
):
    """Get a single Arkham Horror card by code"""
    try:
        card = await app_service.get_card(card_code)

        # If it's an investigator, add basic stats
        if card.type_code == "investigator":
            try:
                stats = await card_service.get_investigator_stats(card_code)
                if stats and "deck_composition" in stats and "meta_position" in stats:
                    # Deck size stats
                    card.average_deck_size = stats["deck_composition"].get("average_deck_size")
                    deck_size_range = stats["deck_composition"].get("deck_size_range", [])
                    if deck_size_range and len(deck_size_range) >= 2:
                        card.deck_size_min = deck_size_range[0]
                        card.deck_size_max = deck_size_range[1]

                    # Popularity stats
                    card.meta_share = stats["meta_position"].get("meta_share")
                    card.total_decks = stats["meta_position"].get("total_decks")
                    card.total_decks_analyzed = stats["meta_position"].get("total_decks_analyzed")
            except Exception as e:
                # If stats fail, just return card without stats
                print(f"Warning: Could not fetch investigator stats for {card_code}: {e}")

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


@router.get("/{card_code}/stats")
async def get_card_stats(
    card_code: str = Depends(get_card_code_param),
    card_service: CardService = Depends(get_card_service),
):
    try:
        """Get stats for a card"""
        return await card_service.get_card_stats(card_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting card stats: {e}")


@router.get("/investigator/{card_code}/stats")
async def get_investigator_stats(
    # investigator_code: str,
    card_code: str = Depends(get_investigator_code_param),
    card_service: CardService = Depends(get_card_service),
):
    print("investigator_code is", card_code)
    """Get stats for an investigator"""
    return await card_service.get_investigator_stats(card_code)


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
