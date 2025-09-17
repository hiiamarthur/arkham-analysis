"""
Scoring endpoints for card evaluation
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, Optional
from pydantic import BaseModel

from app.api.deps import (
    get_base_scoring_service,
    get_conservative_scoring_service,
    get_aggressive_scoring_service,
    get_tempo_scoring_service,
    get_control_scoring_service,
    get_combo_scoring_service,
)
from app.services.app_service import AppService
from app.api.v1.endpoints import get_validated_app_service
from scoring_model.services import (
    BaseCardScoringService,
    ConservativeScoringService,
    AggressiveScoringService,
    TempoScoringService,
    ControlScoringService,
    ComboScoringService,
)

router = APIRouter()


def get_scorer_by_strategy(
    strategy: str,
    base_scorer: BaseCardScoringService,
    conservative_scorer: ConservativeScoringService,
    aggressive_scorer: AggressiveScoringService,
    tempo_scorer: TempoScoringService,
    control_scorer: ControlScoringService,
    combo_scorer: ComboScoringService,
) -> tuple[BaseCardScoringService, str]:
    """Get scorer and strategy name based on strategy parameter"""
    strategy_map = {
        "conservative": (conservative_scorer, "Conservative"),
        "aggressive": (aggressive_scorer, "Aggressive"),
        "tempo": (tempo_scorer, "Tempo"),
        "control": (control_scorer, "Control"),
        "combo": (combo_scorer, "Combo"),
    }

    return strategy_map.get(strategy, (base_scorer, "Base"))


class CardScoreResponse(BaseModel):
    """Response model for card scoring"""

    card_code: str
    card_name: str
    card_type: str
    cost: float
    gain: float
    net_value: float
    scoring_strategy: str


class BulkScoreResponse(BaseModel):
    """Response model for bulk scoring"""

    results: list[CardScoreResponse]
    total_cards: int
    scoring_strategy: str


@router.get("/card/{card_code}", response_model=CardScoreResponse)
async def score_card(
    card_code: str,
    strategy: str = Query(
        "base",
        description="Scoring strategy: base, conservative, aggressive, tempo, control, combo",
    ),
    app_service: AppService = Depends(get_validated_app_service),
    base_scorer: BaseCardScoringService = Depends(get_base_scoring_service),
    conservative_scorer: ConservativeScoringService = Depends(
        get_conservative_scoring_service
    ),
    aggressive_scorer: AggressiveScoringService = Depends(
        get_aggressive_scoring_service
    ),
    tempo_scorer: TempoScoringService = Depends(get_tempo_scoring_service),
    control_scorer: ControlScoringService = Depends(get_control_scoring_service),
    combo_scorer: ComboScoringService = Depends(get_combo_scoring_service),
):
    """Score a single card using the specified strategy"""
    try:
        # Get card from database
        card = await app_service.get_card(card_code)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        # Select scoring strategy
        scorer, strategy_name = get_scorer_by_strategy(
            strategy,
            base_scorer,
            conservative_scorer,
            aggressive_scorer,
            tempo_scorer,
            control_scorer,
            combo_scorer,
        )

        # Calculate scores
        cost = scorer.calculate_cost(card)
        gain = scorer.calculate_gain(card)
        net_value = scorer.calculate_net_value(card)

        return CardScoreResponse(
            card_code=card.code,
            card_name=card.name,
            card_type=card.type_code,
            cost=cost,
            gain=gain,
            net_value=net_value,
            scoring_strategy=strategy_name,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")


@router.post("/cards/bulk", response_model=BulkScoreResponse)
async def score_cards_bulk(
    card_codes: list[str],
    strategy: str = Query(
        "base",
        description="Scoring strategy: base, conservative, aggressive, tempo, control, combo",
    ),
    app_service: AppService = Depends(get_validated_app_service),
    base_scorer: BaseCardScoringService = Depends(get_base_scoring_service),
    conservative_scorer: ConservativeScoringService = Depends(
        get_conservative_scoring_service
    ),
    aggressive_scorer: AggressiveScoringService = Depends(
        get_aggressive_scoring_service
    ),
):
    """Score multiple cards using the specified strategy"""
    try:
        # Select scoring strategy
        if strategy == "conservative":
            scorer = conservative_scorer
            strategy_name = "Conservative"
        elif strategy == "aggressive":
            scorer = aggressive_scorer
            strategy_name = "Aggressive"
        else:
            scorer = base_scorer
            strategy_name = "Base"

        results = []
        for card_code in card_codes:
            try:
                card = await app_service.get_card(card_code)
                if card:
                    cost = scorer.calculate_cost(card)
                    gain = scorer.calculate_gain(card)
                    net_value = scorer.calculate_net_value(card)

                    results.append(
                        CardScoreResponse(
                            card_code=card.code,
                            card_name=card.name,
                            card_type=card.type_code,
                            cost=cost,
                            gain=gain,
                            net_value=net_value,
                            scoring_strategy=strategy_name,
                        )
                    )
            except Exception as e:
                # Skip cards that can't be scored
                continue

        return BulkScoreResponse(
            results=results, total_cards=len(results), scoring_strategy=strategy_name
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk scoring failed: {str(e)}")


@router.get("/encounter/{encounter_id}/cards", response_model=BulkScoreResponse)
async def score_encounter_cards(
    encounter_id: int,
    strategy: str = Query(
        "base",
        description="Scoring strategy: base, conservative, aggressive, tempo, control, combo",
    ),
    app_service: AppService = Depends(get_validated_app_service),
    base_scorer: BaseCardScoringService = Depends(get_base_scoring_service),
    conservative_scorer: ConservativeScoringService = Depends(
        get_conservative_scoring_service
    ),
    aggressive_scorer: AggressiveScoringService = Depends(
        get_aggressive_scoring_service
    ),
):
    """Score all cards from a specific encounter set"""
    try:
        # Get cards from encounter
        cards = await app_service.get_cards_by_encounter(encounter_id)

        # Select scoring strategy
        if strategy == "conservative":
            scorer = conservative_scorer
            strategy_name = "Conservative"
        elif strategy == "aggressive":
            scorer = aggressive_scorer
            strategy_name = "Aggressive"
        else:
            scorer = base_scorer
            strategy_name = "Base"

        results = []
        for card in cards:
            try:
                cost = scorer.calculate_cost(card)
                gain = scorer.calculate_gain(card)
                net_value = scorer.calculate_net_value(card)

                results.append(
                    CardScoreResponse(
                        card_code=card.code,
                        card_name=card.name,
                        card_type=card.type_code,
                        cost=cost,
                        gain=gain,
                        net_value=net_value,
                        scoring_strategy=strategy_name,
                    )
                )
            except Exception as e:
                # Skip cards that can't be scored
                continue

        return BulkScoreResponse(
            results=results, total_cards=len(results), scoring_strategy=strategy_name
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Encounter scoring failed: {str(e)}"
        )


@router.get("/strategies")
async def get_scoring_strategies():
    """Get available scoring strategies"""
    return {
        "strategies": [
            {
                "name": "base",
                "description": "Balanced scoring with default weights",
                "focus": "General purpose evaluation",
            },
            {
                "name": "conservative",
                "description": "Conservative scoring that values safety and efficiency",
                "focus": "Survival and resource management",
            },
            {
                "name": "aggressive",
                "description": "Aggressive scoring that values power and tempo",
                "focus": "Speed and maximum impact",
            },
            {
                "name": "tempo",
                "description": "Tempo-focused scoring that values speed and efficiency",
                "focus": "Fast actions and immediate impact",
            },
            {
                "name": "control",
                "description": "Control-focused scoring that values long-term value",
                "focus": "Resource efficiency and sustainability",
            },
            {
                "name": "combo",
                "description": "Combo-focused scoring that values synergy",
                "focus": "Card interactions and combinations",
            },
        ]
    }
