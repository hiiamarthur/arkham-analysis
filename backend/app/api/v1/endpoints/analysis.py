from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

from app.schemas.context_schema import GameContextSchema
from app.services.analysis_service import AnalysisService
from app.api.deps import get_analysis_service

# Import shared utilities
from . import (
    ARKHAM_HEADERS,
)

router = APIRouter()


class CardAnalysisRequest(BaseModel):
    """Request for context-aware card analysis"""

    card_codes: List[str] = Field(description="Cards to analyze")
    game_context: Optional[GameContextSchema] = Field(
        default=None, description="Current game state for contextual analysis"
    )
    investigator_code: Optional[str] = Field(
        default=None, description="Investigator context for analysis"
    )
    campaign_context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Campaign-specific context (difficulty, special rules, etc.)",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "card_codes": ["01030", "01031", "01032"],
                "investigator_code": "01001",
                "campaign_context": {
                    "campaign": "night_of_the_zealot",
                    "difficulty": "standard",
                },
                "game_context": {
                    "current_scenario": "01104",
                    "doom_on_agenda": 3,
                    "doom_threshold": 6,
                    "investigators": [
                        {
                            "investigator_code": "01001",
                            "current_health": 7,
                            "max_health": 9,
                            "current_resources": 2,
                        }
                    ],
                    "active_investigator": "01001",
                    "analysis_question": "Which cards should I prioritize playing?",
                },
            }
        }


class AnalysisResponse(BaseModel):
    """Response containing comprehensive analysis"""

    success: bool
    message: str
    analysis: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Analysis completed successfully",
                "analysis": {
                    "analysis_type": "comprehensive_game_analysis",
                    "threat_assessment": {
                        "overall_threat_level": 0.6,
                        "threat_description": "High - Dangerous situation",
                    },
                    "gpt_analysis": "Based on the current situation...",
                    "recommended_actions": [
                        {
                            "priority": "HIGH",
                            "action": "evade_enemy",
                            "description": "Enemy is dangerous, consider evading",
                        }
                    ],
                },
            }
        }


@router.post("/card-strength", response_model=AnalysisResponse)
async def analyze_card_strength(
    request: CardAnalysisRequest,
    response: Response,
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    """
    Analyze card strength using context-aware GPT analysis.
    The context modifies how GPT evaluates card power and value.
    """
    try:
        analysis_result = await analysis_service.analyze_card_strength(
            card_codes=request.card_codes,
            game_context=request.game_context,
            investigator_code=request.investigator_code,
            campaign_context=request.campaign_context,
        )

        response.headers.update(ARKHAM_HEADERS)
        response.headers["Cache-Control"] = f"private, max-age=300"  # 5 minutes

        return AnalysisResponse(
            success=True,
            message="Card strength analysis completed successfully",
            analysis=analysis_result,
        )

    except Exception as e:
        print(f"Error analyzing card strength: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Card strength analysis failed: {str(e)}",
        )


@router.post("/card-synergies", response_model=AnalysisResponse)
async def analyze_card_synergies(
    request: CardAnalysisRequest,
    response: Response,
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    """
    Analyze synergies between cards with investigator and campaign context.
    Focus on combos, interactions, and optimal card combinations.
    """
    try:
        analysis_result = await analysis_service.analyze_card_synergies(
            card_codes=request.card_codes,
            investigator_code=request.investigator_code,
            campaign_context=request.campaign_context,
        )

        response.headers.update(ARKHAM_HEADERS)
        response.headers["Cache-Control"] = f"private, max-age=600"  # 10 minutes

        return AnalysisResponse(
            success=True,
            message="Card synergy analysis completed",
            analysis=analysis_result,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Card synergy analysis failed: {str(e)}",
        )


@router.post("/card-timing", response_model=AnalysisResponse)
async def analyze_card_timing(
    request: CardAnalysisRequest,
    response: Response,
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    """
    Analyze optimal timing for playing cards based on current game state.
    Considers urgency, resource costs, and maximum impact scenarios.
    """
    try:
        analysis_result = await analysis_service.analyze_card_timing(
            card_codes=request.card_codes,
            game_context=request.game_context,
            investigator_code=request.investigator_code,
        )

        response.headers.update(ARKHAM_HEADERS)
        response.headers["Cache-Control"] = f"private, max-age=60"  # 1 minute

        return AnalysisResponse(
            success=True,
            message="Card timing analysis completed",
            analysis=analysis_result,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Card timing analysis failed: {str(e)}",
        )


@router.get("/threat-assessment")
async def get_threat_assessment(
    scenario: str,
    act: int,
    agenda: int,
    doom_on_agenda: int,
    doom_threshold: int,
    response: Response,
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    """
    Quick threat assessment endpoint for monitoring game danger level
    without full GPT analysis.
    """
    try:
        # Create minimal game context for threat assessment
        minimal_context = GameContextSchema(
            current_scenario=scenario,
            current_act=act,
            current_agenda=agenda,
            doom_on_agenda=doom_on_agenda,
            doom_threshold=doom_threshold,
            investigators=[],  # Empty for quick assessment
            active_investigator="",
            analysis_question="Threat assessment",
        )

        threat_assessment = analysis_service.context_service.calculate_threat_level(
            minimal_context
        )

        response.headers.update(ARKHAM_HEADERS)
        response.headers["Cache-Control"] = f"public, max-age=60"  # 1 minute

        return {
            "success": True,
            "threat_assessment": threat_assessment,
            "scenario_info": {
                "scenario": scenario,
                "act": act,
                "agenda": agenda,
                "doom_pressure": f"{doom_on_agenda}/{doom_threshold}",
            },
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Threat assessment failed: {str(e)}",
        )
