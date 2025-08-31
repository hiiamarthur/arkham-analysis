from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, Text, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional, Dict, Any


class EncounterSetModel(BaseModel):
    __tablename__ = "encounter_sets"

    code: Mapped[str] = mapped_column(String(50), primary_key=True, unique=True)
    name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    scenario_codes: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)  # Scenarios that use this set
    pack_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Relationships
    cards: Mapped[List["EncounterCardModel"]] = relationship(
        "EncounterCardModel", back_populates="encounter_set"
    )


class EncounterCardModel(BaseModel):
    __tablename__ = "encounter_cards"

    code: Mapped[str] = mapped_column(String(50), primary_key=True, unique=True)
    name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    encounter_code: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("encounter_sets.code"), nullable=True)
    type_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # enemy, treachery, location
    subtype_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pack_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    quantity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=1)
    
    # Enemy-specific stats
    health: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    health_per_investigator: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    fight: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    evade: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    damage: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    horror: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Location-specific stats  
    shroud: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    clues: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    clues_per_investigator: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Additional properties
    traits: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    victory: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    vengeance: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    doom: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Relationships
    encounter_set: Mapped[Optional[EncounterSetModel]] = relationship(
        "EncounterSetModel", back_populates="cards"
    )


class ScenarioModel(BaseModel):
    __tablename__ = "scenarios"
    
    code: Mapped[str] = mapped_column(String(50), primary_key=True, unique=True)
    name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    campaign: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    pack_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Scenario mechanics
    encounter_set_codes: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    doom_threshold: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    agenda_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    act_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Chaos bag composition (by difficulty)
    chaos_bag_easy: Mapped[Optional[Dict[str, int]]] = mapped_column(JSON, nullable=True)
    chaos_bag_standard: Mapped[Optional[Dict[str, int]]] = mapped_column(JSON, nullable=True)
    chaos_bag_hard: Mapped[Optional[Dict[str, int]]] = mapped_column(JSON, nullable=True)
    chaos_bag_expert: Mapped[Optional[Dict[str, int]]] = mapped_column(JSON, nullable=True)
    
    # Calculated context (cached for performance)
    context_cache: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    context_updated_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)