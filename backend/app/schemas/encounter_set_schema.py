"""
Pydantic schemas for encounter sets
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class EncounterSetBase(BaseModel):
    """Base encounter set schema"""

    code: str = Field(..., description="Unique encounter set code")
    name: str = Field(..., description="Display name of the encounter set")
    pack_code: Optional[str] = Field(
        None, description="Pack code this encounter set belongs to"
    )
    pack_name: Optional[str] = Field(
        None, description="Pack name this encounter set belongs to"
    )
    cycle_name: Optional[str] = Field(
        None, description="Cycle name this encounter set belongs to"
    )
    size: Optional[int] = Field(
        None, description="Number of cards in the encounter set"
    )
    is_unique: bool = Field(
        False, description="Whether this is a unique/story encounter set"
    )


class EncounterSet(EncounterSetBase):
    """Full encounter set schema with computed fields"""

    id: int
    card_count: int = Field(
        0, description="Actual number of cards linked to this encounter set"
    )

    class Config:
        from_attributes = True

    @classmethod
    def from_model(cls, encounter_set_model):
        """Convert from database model"""
        from app.models.arkham_model import EncounterSetModel

        if not isinstance(encounter_set_model, EncounterSetModel):
            raise ValueError("Expected EncounterSetModel instance")

        return cls(
            id=encounter_set_model.id,
            code=encounter_set_model.code,
            name=encounter_set_model.name,
            pack_code=encounter_set_model.pack_code,
            pack_name=encounter_set_model.pack_name,
            cycle_name=encounter_set_model.cycle_name,
            size=encounter_set_model.size,
            is_unique=encounter_set_model.is_unique,
            card_count=(
                len(encounter_set_model.cards) if encounter_set_model.cards else 0
            ),
        )


class EncounterSetCreate(EncounterSetBase):
    """Schema for creating encounter sets"""

    pass


class EncounterSetUpdate(BaseModel):
    """Schema for updating encounter sets"""

    name: Optional[str] = None
    pack_code: Optional[str] = None
    pack_name: Optional[str] = None
    cycle_name: Optional[str] = None
    size: Optional[int] = None
    is_unique: Optional[bool] = None


class EncounterSetSummary(BaseModel):
    """Lightweight encounter set summary"""

    code: str
    name: str
    cycle_name: Optional[str]
    card_count: int


class EncounterSetWithCards(EncounterSet):
    """Encounter set with card details"""

    cards: List[Dict[str, Any]] = Field(
        default_factory=list, description="Cards in this encounter set"
    )

    @classmethod
    def from_model_with_cards(cls, encounter_set_model):
        """Convert from database model including card details"""
        from app.schemas.card_schema import CardSchema

        base_data = EncounterSet.from_model(encounter_set_model)

        cards = []
        if encounter_set_model.cards:
            for card in encounter_set_model.cards:
                try:
                    card_data = CardSchema.from_model(card)
                    cards.append(card_data.model_dump())
                except Exception:
                    # Skip problematic cards
                    continue

        return cls(**base_data.model_dump(), cards=cards)
