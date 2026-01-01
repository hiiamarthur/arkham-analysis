from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app.database import get_db
from app.services.scenario_context_service import scenario_context_service
from app.models.encounter_model import (
    ScenarioModel,
    EncounterScenarioSetModel,
    EncounterCardModel,
)
from pydantic import BaseModel


# Response models
class ScenarioContextResponse(BaseModel):
    scenario_code: str
    scenario_name: str
    difficulty: str
    context: Dict[str, Any]


class EncounterCardResponse(BaseModel):
    code: str
    name: Optional[str]
    type_code: Optional[str]
    encounter_code: Optional[str]
    health: Optional[int]
    fight: Optional[int]
    evade: Optional[int]
    damage: Optional[int]
    horror: Optional[int]
    shroud: Optional[int]
    clues: Optional[int]
    traits: Optional[List[str]]


router = APIRouter(prefix="/scenarios", tags=["scenarios"])


@router.get("/{scenario_code}/context")
async def get_scenario_context(
    scenario_code: str, difficulty: str = "Standard", db: Session = Depends(get_db)
) -> ScenarioContextResponse:
    """Get scenario context for card evaluation"""
    try:
        context = await scenario_context_service.get_scenario_context(
            scenario_code, difficulty
        )

        return ScenarioContextResponse(
            scenario_code=scenario_code,
            scenario_name=context.get("scenario_name", "Unknown"),
            difficulty=difficulty,
            context=context,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get scenario context: {str(e)}"
        )


@router.get("/{scenario_code}/context/raw")
async def get_raw_scenario_context(
    scenario_code: str, difficulty: str = "Standard"
) -> Dict[str, Any]:
    """Get raw scenario context data"""
    return await scenario_context_service.get_scenario_context(
        scenario_code, difficulty
    )


@router.get("/")
async def list_scenarios(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """List all available scenarios"""
    scenarios = db.query(ScenarioModel).all()
    return [
        {
            "code": scenario.code,
            "name": scenario.name,
            "campaign": scenario.campaign,
            "pack_code": scenario.pack_code,
            "has_context": scenario.context_cache is not None,
        }
        for scenario in scenarios
    ]


@router.get("/{scenario_code}/encounter-cards")
async def get_scenario_encounter_cards(
    scenario_code: str, db: Session = Depends(get_db)
) -> List[EncounterCardResponse]:
    """Get all encounter cards for a scenario"""
    try:
        # Get scenario context to find encounter sets
        context = await scenario_context_service.get_scenario_context(scenario_code)
        encounter_sets = context.get("encounter_sets", [])

        if not encounter_sets:
            return []

        # Query encounter cards from those sets
        encounter_cards = (
            db.query(EncounterCardModel)
            .filter(EncounterCardModel.encounter_code.in_(encounter_sets))
            .all()
        )

        return [
            EncounterCardResponse(
                code=card.code,
                name=card.name,
                type_code=card.type_code,
                encounter_code=card.encounter_code,
                health=card.health,
                fight=card.fight,
                evade=card.evade,
                damage=card.damage,
                horror=card.horror,
                shroud=card.shroud,
                clues=card.clues,
                traits=card.traits,
            )
            for card in encounter_cards
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get encounter cards: {str(e)}"
        )


@router.post("/populate-encounter-data")
async def populate_encounter_data(
    background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    """Populate encounter card data from ArkhamDB (background task)"""
    try:
        background_tasks.add_task(
            scenario_context_service.populate_encounter_cards_from_arkhamdb
        )
        return {"message": "Encounter data population started in background"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to start population: {str(e)}"
        )


@router.post("/refresh-cache/{scenario_code}")
async def refresh_scenario_cache(scenario_code: str, background_tasks: BackgroundTasks):
    """Refresh scenario context cache"""
    try:
        background_tasks.add_task(
            scenario_context_service.refresh_scenario_cache, scenario_code
        )
        return {"message": f"Cache refresh started for scenario {scenario_code}"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to refresh cache: {str(e)}"
        )


@router.post("/refresh-cache")
async def refresh_all_scenario_caches(background_tasks: BackgroundTasks):
    """Refresh all scenario context caches"""
    try:
        background_tasks.add_task(scenario_context_service.refresh_scenario_cache)
        return {"message": "Cache refresh started for all scenarios"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to refresh caches: {str(e)}"
        )


@router.get("/encounter-sets")
async def list_encounter_sets(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """List all encounter sets"""
    encounter_sets = db.query(EncounterScenarioSetModel).all()
    return [
        {
            "code": set_obj.code,
            "name": set_obj.name,
            "card_count": len(set_obj.cards) if set_obj.cards else 0,
        }
        for set_obj in encounter_sets
    ]


@router.get("/encounter-sets/{set_code}/cards")
async def get_encounter_set_cards(
    set_code: str, db: Session = Depends(get_db)
) -> List[EncounterCardResponse]:
    """Get all cards from an encounter set"""
    cards = (
        db.query(EncounterCardModel)
        .filter(EncounterCardModel.encounter_code == set_code)
        .all()
    )

    return [
        EncounterCardResponse(
            code=card.code,
            name=card.name,
            type_code=card.type_code,
            encounter_code=card.encounter_code,
            health=card.health,
            fight=card.fight,
            evade=card.evade,
            damage=card.damage,
            horror=card.horror,
            shroud=card.shroud,
            clues=card.clues,
            traits=card.traits,
        )
        for card in cards
    ]


# Example usage endpoint - shows how to use scenario context in card evaluation
@router.post("/evaluate-card-in-context")
async def evaluate_card_in_context(
    card_code: str, scenario_code: str, difficulty: str = "Standard"
) -> Dict[str, Any]:
    """Example endpoint showing how to evaluate a card with scenario context"""
    try:
        # Get scenario context
        scenario_context = await scenario_context_service.get_scenario_context(
            scenario_code, difficulty
        )

        # This would integrate with your existing BaseEvaluator
        # For now, just return the context that would be used
        return {
            "card_code": card_code,
            "scenario_context": scenario_context,
            "evaluation_note": "This endpoint would integrate with BaseEvaluator.evaluate_card_strength() using the scenario context",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")
