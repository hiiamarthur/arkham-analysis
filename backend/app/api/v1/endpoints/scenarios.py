from fastapi import APIRouter, Depends, Response, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator

from app.api.deps import get_scenario_service
from app.services.scenario_service import ScenarioService

# Import shared utilities from endpoints __init__.py
from . import (
    get_validated_app_service,
    get_pagination_params,
    PaginatedCardResponse,
    ARKHAM_HEADERS,
    CACHE_TTL_MEDIUM,
)

# Import shared domain types
from domain import (
    Difficulty,
    CampaignType,
    ScenarioType,
    get_scenario_modifications,
)

router = APIRouter(tags=["scenarios"])


# ==================================================================================
# SCENARIO-SPECIFIC REQUEST/RESPONSE MODELS (for POST requests)
# ==================================================================================
# Note: GET requests use Query/Path parameters, not request body models


class ScenarioAnalysisRequest(BaseModel):
    """Request for detailed scenario analysis"""

    scenario_code: str = Field(
        ..., min_length=3, max_length=50, description="Scenario identifier"
    )
    difficulty: Difficulty = Field(Difficulty.STANDARD, description="Difficulty level")
    include_probabilities: bool = Field(
        False, description="Include chaos bag probability calculations"
    )
    investigator_count: Optional[int] = Field(
        None, ge=1, le=4, description="Number of investigators"
    )

    class Config:
        schema_extra = {
            "example": {
                "scenario_code": "the_gathering",
                "difficulty": "expert",
                "include_probabilities": True,
                "investigator_count": 2,
            }
        }


class ChaosBagSimulationRequest(BaseModel):
    """Request for chaos bag simulation"""

    num_draws: int = Field(
        100, ge=1, le=10000, description="Number of token draws to simulate"
    )
    with_bless_curse: bool = Field(
        False, description="Include bless/curse tokens if available"
    )
    seed: Optional[int] = Field(
        None, description="Random seed for reproducible results"
    )


class ScenarioComparisonRequest(BaseModel):
    """Request for comparing multiple scenarios"""

    scenario_codes: List[str] = Field(
        ..., description="List of scenario codes to compare"
    )
    difficulty: Difficulty = Field(
        Difficulty.STANDARD, description="Difficulty level for comparison"
    )
    metrics: List[str] = Field(
        ["token_modifications", "average_difficulty"], description="Metrics to compare"
    )

    @validator("scenario_codes")
    def validate_scenario_codes(cls, v):
        if len(v) < 2:
            raise ValueError("Must provide at least 2 scenario codes")
        if len(v) > 8:
            raise ValueError("Cannot compare more than 8 scenarios at once")
        return v


# Response models specific to scenarios
class ScenarioDetail(BaseModel):
    """Detailed scenario information"""

    code: str
    name: str
    campaign: str
    campaign_name: str
    difficulty_available: List[str] = Field(
        default_factory=lambda: [d.value for d in Difficulty]
    )


class TokenModificationDetail(BaseModel):
    """Detailed token modification information"""

    token_type: str
    effect: str
    value: Any
    additional_effects: Optional[Dict[str, Any]] = None


@router.get("/", response_model=List[Dict[str, Any]])
async def get_all_scenarios(
    response: Response,
    campaign: Optional[CampaignType] = Query(None, description="Filter by campaign"),
):
    """Get all available scenarios, optionally filtered by campaign"""

    scenarios = []
    scenario_list = (
        ScenarioType.from_campaign(campaign) if campaign else list(ScenarioType)
    )

    for scenario in scenario_list:
        scenarios.append(
            {
                "code": scenario.scenario_code,
                "name": scenario.display_name,
                "campaign": scenario.campaign.value,
                "campaign_name": scenario.campaign.display_name,
            }
        )

    response.headers.update(ARKHAM_HEADERS)
    response.headers["Cache-Control"] = f"public, max-age={CACHE_TTL_MEDIUM}"

    return scenarios


@router.get("/campaigns", response_model=List[Dict[str, Any]])
async def get_all_campaigns(response: Response):
    """Get all available campaigns"""

    campaigns = []
    for campaign in CampaignType:
        scenario_count = len(ScenarioType.from_campaign(campaign))
        campaigns.append(
            {
                "code": campaign.value,
                "name": campaign.display_name,
                "scenario_count": scenario_count,
            }
        )

    response.headers.update(ARKHAM_HEADERS)
    response.headers["Cache-Control"] = f"public, max-age={CACHE_TTL_MEDIUM}"

    return campaigns


@router.get("/{scenario_code}/chaos-tokens", response_model=Dict[str, Any])
async def get_scenario_chaos_tokens(
    response: Response,
    scenario_code: str,
    difficulty: Difficulty = Query(
        Difficulty.STANDARD, description="Scenario difficulty"
    ),
):
    """Get chaos token modifications for a specific scenario and difficulty"""

    # Find scenario by code
    scenario = None
    for s in ScenarioType:
        if s.scenario_code == scenario_code:
            scenario = s
            break

    if not scenario:
        from . import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenario not found: {scenario_code}",
        )

    # Get scenario modifications
    modifications = get_scenario_modifications(scenario, difficulty)

    response.headers.update(ARKHAM_HEADERS)
    response.headers["Cache-Control"] = f"public, max-age={CACHE_TTL_MEDIUM}"

    return {
        "scenario": {
            "code": scenario.scenario_code,
            "name": scenario.display_name,
            "campaign": scenario.campaign.value,
        },
        "difficulty": difficulty.value,
        "token_modifications": modifications,
        "has_modifications": len(modifications) > 0,
    }


@router.get("/context", response_model=Dict[str, Any])
async def get_scenario_context(
    response: Response,
    scenario_code: ScenarioType,  # ✅ Path parameter
    difficulty: Difficulty = Query(
        Difficulty.STANDARD, description="Difficulty level"
    ),  # ✅ Query parameter
    no_of_investigators: int = Query(
        4, ge=1, le=4, description="Number of investigators"
    ),  # ✅ Query parameter
    scenario_context_service: ScenarioService = Depends(get_scenario_service),
):
    """Get context for a specific scenario and difficulty"""
    # Use individual parameters instead of request body
    return await scenario_context_service.yield_scenario_context(
        scenario_code, difficulty, no_of_investigators
    )


@router.get("/{scenario_code}/cards", response_model=PaginatedCardResponse)
async def get_scenario_cards(
    response: Response,
    scenario_code: str,
    pagination=Depends(get_pagination_params),
    app_service=Depends(get_validated_app_service),
):
    """Get cards associated with a specific scenario"""

    # This would need to be implemented in your app service
    # For now, return empty result
    response.headers.update(ARKHAM_HEADERS)
    response.headers["Cache-Control"] = f"public, max-age={CACHE_TTL_MEDIUM}"

    return PaginatedCardResponse(
        cards=[],
        pagination={
            "page": pagination["page"],
            "limit": pagination["limit"],
            "has_next": False,
            "has_prev": pagination["page"] > 1,
        },
        filters={"scenario": scenario_code},
        total_results=0,
    )


@router.get("/{scenario_code}/difficulty-comparison", response_model=Dict[str, Any])
async def compare_scenario_difficulties(
    response: Response,
    scenario_code: str,
):
    """Compare chaos token modifications across all difficulties for a scenario"""

    # Find scenario by code
    scenario = None
    for s in ScenarioType:
        if s.scenario_code == scenario_code:
            scenario = s
            break

    if not scenario:
        from . import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenario not found: {scenario_code}",
        )

    difficulty_comparison = {}
    for difficulty in Difficulty:
        modifications = get_scenario_modifications(scenario, difficulty)
        difficulty_comparison[difficulty.value] = {
            "difficulty_name": difficulty.display_name,
            "token_modifications": modifications,
            "modification_count": len(modifications),
        }

    response.headers.update(ARKHAM_HEADERS)
    response.headers["Cache-Control"] = f"public, max-age={CACHE_TTL_MEDIUM}"

    return {
        "scenario": {
            "code": scenario.scenario_code,
            "name": scenario.display_name,
            "campaign": scenario.campaign.value,
        },
        "difficulties": difficulty_comparison,
    }


@router.post("/{scenario_code}/analyze", response_model=Dict[str, Any])
async def analyze_scenario_advanced(
    scenario_code: str,
    analysis_request: ScenarioAnalysisRequest,  # ✅ Endpoint-specific request class
    app_service=Depends(get_validated_app_service),
):
    """Advanced scenario analysis with customizable parameters"""

    # Find scenario by code
    scenario = None
    for s in ScenarioType:
        if s.scenario_code == scenario_code:
            scenario = s
            break

    if not scenario:
        from . import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenario not found: {scenario_code}",
        )

    # Get modifications for the requested difficulty
    modifications = get_scenario_modifications(scenario, analysis_request.difficulty)

    # Build analysis response
    analysis = {
        "scenario": {
            "code": scenario.scenario_code,
            "name": scenario.display_name,
            "campaign": scenario.campaign.value,
        },
        "analysis_parameters": {
            "difficulty": analysis_request.difficulty.value,
            "investigator_count": analysis_request.investigator_count,
            "include_probabilities": analysis_request.include_probabilities,
        },
        "token_modifications": modifications,
        "modification_count": len(modifications),
    }

    # Add probability calculations if requested
    if analysis_request.include_probabilities:
        analysis["probability_analysis"] = {
            "note": "Probability calculations would be implemented here",
            "average_modifier": -1.5,  # Placeholder
            "success_rates": {"skill_3": 0.65, "skill_4": 0.75, "skill_5": 0.85},
        }

    return analysis


@router.post("/{scenario_code}/simulate-chaos-bag", response_model=Dict[str, Any])
async def simulate_chaos_bag(
    scenario_code: str,
    difficulty: Difficulty,
    simulation_request: ChaosBagSimulationRequest,  # ✅ Endpoint-specific request class
):
    """Simulate chaos bag draws for statistical analysis"""

    # Find scenario
    scenario = None
    for s in ScenarioType:
        if s.scenario_code == scenario_code:
            scenario = s
            break

    if not scenario:
        from . import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenario not found: {scenario_code}",
        )

    # This would integrate with your scoring model's chaos bag simulation
    # For now, return a mock response
    import random

    if simulation_request.seed:
        random.seed(simulation_request.seed)

    # Mock simulation results
    results = {
        "scenario": {
            "code": scenario.scenario_code,
            "name": scenario.display_name,
            "difficulty": difficulty.value,
        },
        "simulation_parameters": {
            "num_draws": simulation_request.num_draws,
            "with_bless_curse": simulation_request.with_bless_curse,
            "seed": simulation_request.seed,
        },
        "results": {
            "average_modifier": round(random.uniform(-2.5, 0.5), 2),
            "token_distribution": {
                "positive": random.randint(10, 25),
                "zero": random.randint(15, 30),
                "negative": random.randint(45, 75),
            },
            "special_tokens_drawn": random.randint(8, 15),
        },
    }

    return results


@router.post("/compare", response_model=Dict[str, Any])
async def compare_scenarios(
    comparison_request: ScenarioComparisonRequest,  # ✅ Endpoint-specific request class
):
    """Compare multiple scenarios across various metrics"""

    scenarios_data = []

    for scenario_code in comparison_request.scenario_codes:
        # Find scenario
        scenario = None
        for s in ScenarioType:
            if s.scenario_code == scenario_code:
                scenario = s
                break

        if scenario:
            modifications = get_scenario_modifications(
                scenario, comparison_request.difficulty
            )
            scenarios_data.append(
                {
                    "code": scenario.scenario_code,
                    "name": scenario.display_name,
                    "campaign": scenario.campaign.value,
                    "token_modifications": len(modifications),
                    "has_skull_effects": "skull" in modifications,
                    "has_special_tokens": any(
                        token in modifications
                        for token in ["cultist", "tablet", "elder_thing"]
                    ),
                }
            )

    return {
        "comparison_parameters": {
            "difficulty": comparison_request.difficulty.value,
            "metrics": comparison_request.metrics,
            "scenarios_compared": len(scenarios_data),
        },
        "scenarios": scenarios_data,
        "summary": {
            "average_modifications": (
                sum(s["token_modifications"] for s in scenarios_data)
                / len(scenarios_data)
                if scenarios_data
                else 0
            ),
            "scenarios_with_skull": sum(
                1 for s in scenarios_data if s["has_skull_effects"]
            ),
            "scenarios_with_special": sum(
                1 for s in scenarios_data if s["has_special_tokens"]
            ),
        },
    }
