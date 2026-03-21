"""
Shared utilities, dependencies, and models for all Arkham Analysis endpoints
"""

from fastapi import Depends, HTTPException, Query, Path, Header, status
from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, Field, validator
from enum import Enum
from datetime import datetime, timedelta
from app.api.deps import get_app_service, get_cache_service
from app.services.app_service import AppService
from app.core.config import settings


def seconds_until_next_sunday_midnight() -> int:
    """Returns TTL in seconds so the cache expires at next Sunday 00:00 UTC."""
    now = datetime.utcnow()
    days_ahead = (6 - now.weekday()) % 7 or 7
    next_sunday = (now + timedelta(days=days_ahead)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    return max(int((next_sunday - now).total_seconds()), 3600)

# Import shared domain types
from domain import CardType, Faction, Difficulty, CampaignType, ScenarioType


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class SortField(str, Enum):
    NAME = "name"
    COST = "cost"
    XP = "xp"
    FACTION = "faction_code"
    TYPE = "type_code"
    SCORE = "score"


# =============================================================================
# SHARED DEPENDENCIES
# =============================================================================


async def get_validated_app_service(
    app_service: AppService = Depends(get_app_service),
) -> AppService:
    """App service with validation for Arkham endpoints"""
    return app_service


def get_card_code_param(
    card_code: str = Path(
        ...,
        min_length=5,
        max_length=10,
        regex=r"^[0-9]{5}[a-z]?$",
        description="Arkham card code (e.g., '01001', '02110a')",
    )
) -> str:
    """Validate and format Arkham card code"""
    return card_code.lower()


def get_investigator_code_param(
    card_code: str = Path(
        ...,
        min_length=5,
        max_length=10,
        regex=r"^[0-9]{5}[a-z]?$",
        description="Arkham investigator code (e.g., '01001', '02110a')",
    )
) -> str:
    """Validate and format Arkham investigator code"""
    return card_code.lower()


def get_encounter_param(
    encounter: int = Path(
        ..., ge=0, le=50, description="Encounter set ID (0 for player cards)"
    )
) -> int:
    """Validate encounter set parameter"""
    return encounter


def get_pagination_params(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
) -> Dict[str, int]:
    """Standard pagination parameters"""
    return {"page": page, "limit": limit}


def get_search_params(
    q: str = Query(..., min_length=2, max_length=100, description="Search query"),
    faction: Optional[Faction] = Query(None, description="Filter by faction"),
    card_type: Optional[CardType] = Query(None, description="Filter by card type"),
    min_xp: Optional[int] = Query(None, ge=0, le=5, description="Minimum XP level"),
    max_xp: Optional[int] = Query(None, ge=0, le=5, description="Maximum XP level"),
    min_cost: Optional[int] = Query(None, ge=0, description="Minimum resource cost"),
    max_cost: Optional[int] = Query(
        None, ge=0, le=10, description="Maximum resource cost"
    ),
) -> Dict[str, Any]:
    """Advanced search parameters for Arkham cards"""
    return {
        "query": q.strip(),
        "faction": faction,
        "card_type": card_type,
        "min_xp": min_xp,
        "max_xp": max_xp,
        "min_cost": min_cost,
        "max_cost": max_cost,
    }


def get_sorting_params(
    sort_by: SortField = Query(SortField.NAME, description="Field to sort by"),
    sort_order: SortOrder = Query(SortOrder.ASC, description="Sort order"),
) -> Dict[str, str]:
    """Sorting parameters"""
    return {"sort_by": sort_by.value, "sort_order": sort_order.value}


def get_cache_control_header(
    cache_control: Optional[str] = Header(None, description="Cache control override")
) -> Optional[str]:
    """Optional cache control override"""
    return cache_control


# =============================================================================
# SHARED RESPONSE MODELS
# =============================================================================


class ArkhamApiResponse(BaseModel):
    """Standard Arkham API response format"""

    success: bool
    message: str
    data: Any = None
    arkham_version: str = Field(default="v1", description="API version")
    timestamp: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Card retrieved successfully",
                "data": {"card_code": "01001", "name": "Roland Banks"},
                "arkham_version": "v1",
            }
        }


class CardSummary(BaseModel):
    """Lightweight card summary for lists"""

    code: str
    name: str
    subname: Optional[str] = None
    faction_code: Optional[str]
    type_code: str
    xp: Optional[int] = None
    cost: Optional[int]
    traits: Optional[List[str]]
    pack_code: Optional[str]
    illustrator: Optional[str]


class PaginatedCardResponse(BaseModel):
    """Paginated response for card lists"""

    cards: List[CardSummary]
    pagination: Dict[str, Any] = Field(description="Pagination metadata")
    filters: Dict[str, Any] = Field(description="Applied filters")
    total_results: int

    class Config:
        json_schema_extra = {
            "example": {
                "cards": [
                    {
                        "code": "01001",
                        "name": "Roland Banks",
                        "faction_code": "guardian",
                        "type_code": "investigator",
                    }
                ],
                "pagination": {"page": 1, "limit": 20, "has_next": False},
                "total_results": 1,
            }
        }


class ScoringResult(BaseModel):
    """Card scoring result"""

    card_code: str
    score: float
    algorithm: str = "base_evaluator"
    factors: Dict[str, float] = Field(
        default_factory=dict, description="Scoring factor breakdown"
    )


class SyncStatus(BaseModel):
    """Synchronization operation status"""

    operation: str
    status: str  # "started", "in_progress", "completed", "failed"
    items_processed: int = 0
    total_items: Optional[int] = None
    errors: List[str] = Field(default_factory=list)
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


# =============================================================================
# SHARED EXCEPTIONS
# =============================================================================

CARD_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Card not found in database"
)

INVALID_CARD_CODE = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Arkham card code format"
)

ENCOUNTER_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Encounter set not found"
)

SEARCH_TOO_BROAD = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Search query too broad, please add more specific filters",
)

ARKHAMDB_UNAVAILABLE = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="ArkhamDB service temporarily unavailable",
)

BULK_LIMIT_EXCEEDED = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Bulk operation limit exceeded (max 1000 items)",
)

SCORING_UNAVAILABLE = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="Scoring service temporarily unavailable",
)

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================


def validate_card_codes(card_codes: List[str]) -> List[str]:
    """Validate a list of Arkham card codes"""
    if len(card_codes) > 1000:
        raise BULK_LIMIT_EXCEEDED

    validated = []
    for code in card_codes:
        if not code or len(code) < 5 or len(code) > 10:
            raise INVALID_CARD_CODE
        validated.append(code.lower())

    return validated


def validate_xp_range(min_xp: Optional[int], max_xp: Optional[int]) -> bool:
    """Validate XP range parameters"""
    if min_xp is not None and max_xp is not None:
        if min_xp > max_xp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="min_xp cannot be greater than max_xp",
            )
    return True


def validate_cost_range(min_cost: Optional[int], max_cost: Optional[int]) -> bool:
    """Validate cost range parameters"""
    if min_cost is not None and max_cost is not None:
        if min_cost > max_cost:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="min_cost cannot be greater than max_cost",
            )
    return True


# =============================================================================
# CONSTANTS
# =============================================================================

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
MAX_BULK_SIZE = 1000

# Search
MIN_SEARCH_LENGTH = 2
MAX_SEARCH_LENGTH = 100
MAX_SEARCH_RESULTS = 1000

# Caching
CACHE_TTL_SHORT = 300  # 5 minutes - for dynamic data
CACHE_TTL_MEDIUM = 1800  # 30 minutes - for card data
CACHE_TTL_LONG = 7200  # 2 hours - for static data

# Scoring
DEFAULT_SCORING_ALGORITHM = "base_evaluator"
SUPPORTED_SCORING_ALGORITHMS = ["base_evaluator", "weighted", "advanced"]

# HTTP Headers
ARKHAM_HEADERS = {
    "X-Arkham-API-Version": "v1",
    "X-Arkham-Scoring-Version": "2.0",
    "X-ArkhamDB-Last-Sync": "dynamic",  # Set at runtime
}
