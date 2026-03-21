from app.models.base import BaseModel
from sqlalchemy import (
    JSON,
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Table,
    ForeignKey,
    text,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional, Dict, Any
from datetime import datetime


# Define the association table first
card_traits = Table(
    "card_traits",
    BaseModel.metadata,
    Column(
        "card_code",
        String(50),
        ForeignKey("cards.code", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "trait_name",
        String(100),
        ForeignKey("traits.name", ondelete="CASCADE"),
        primary_key=True,
    ),
)

# Add association table for card-taboo relationship
card_taboos = Table(
    "card_taboos",
    BaseModel.metadata,
    Column("card_code", String(50), ForeignKey("cards.code", ondelete="CASCADE")),
    Column("taboo_id", Integer, ForeignKey("taboos.id", ondelete="CASCADE")),
)

# Association table for card-encounter set relationship
card_encounter_sets = Table(
    "card_encounter_sets",
    BaseModel.metadata,
    Column(
        "card_code",
        String(50),
        ForeignKey("cards.code", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "encounter_set_id",
        Integer,
        ForeignKey("encounter_sets.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class BondedCardModel(BaseModel):
    __tablename__ = "bonded_cards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    card_code: Mapped[str] = mapped_column(
        String(50), ForeignKey("cards.code", ondelete="CASCADE"), nullable=False
    )
    bonded_card_code: Mapped[str] = mapped_column(
        String(50), ForeignKey("cards.code", ondelete="CASCADE"), nullable=False
    )
    count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Relationships
    card: Mapped["CardModel"] = relationship(
        "CardModel", foreign_keys=[card_code], back_populates="bonded_cards"
    )
    bonded_card: Mapped["CardModel"] = relationship(
        "CardModel", foreign_keys=[bonded_card_code]
    )


class TabooModel(BaseModel):
    __tablename__ = "taboos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    taboo_code: Mapped[str] = mapped_column(String(50), nullable=True)
    code: Mapped[str] = mapped_column(String(50), nullable=True)
    text: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    cost: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    cards: Mapped[List["CardModel"]] = relationship(
        "CardModel",
        secondary=card_taboos,
        back_populates="taboo_versions",
        lazy="selectin",  # Change to eager loading
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict without circular references"""
        return {
            "id": self.id,
            "code": self.code,
            "text": self.text,
            "cost": self.cost,
            "level": self.level,
        }


class TraitModel(BaseModel):
    __tablename__ = "traits"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    cards: Mapped[List["CardModel"]] = relationship(
        secondary="card_traits", back_populates="traits"
    )


class EncounterSetModel(BaseModel):
    """
    Encounter set model - stores encounter set information from ArkhamDB

    Examples:
    - Core Set encounter sets (Striking Fear, Ancient Evils, etc.)
    - Campaign-specific encounter sets
    - Standalone scenario encounter sets
    """

    __tablename__ = "encounter_sets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    # Pack and cycle information
    pack_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    pack_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Relationships
    cards: Mapped[List["CardModel"]] = relationship(
        secondary=card_encounter_sets, back_populates="encounter_sets", lazy="selectin"
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for API responses"""
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "pack_code": self.pack_code,
            "pack_name": self.pack_name,
        }

    __table_args__ = {
        "postgresql_with_oids": False
    }  # Ensure PostgreSQL doesn't use OIDs


class CardModel(BaseModel):
    __tablename__ = "cards"

    code: Mapped[str] = mapped_column(String(50), primary_key=True, unique=True)
    name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    real_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    subname: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    cost: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    text: Mapped[Optional[str]] = mapped_column(String(3000), nullable=True)
    real_text: Mapped[Optional[str]] = mapped_column(String(3000), nullable=True)
    type_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    type_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    faction_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    faction_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    faction2_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    faction2_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    faction3_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    faction3_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    subtype_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    subtype_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    tags: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    alternate_of_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    alternate_of_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    pack_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    pack_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    quantity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_unique: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    exceptional: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    myriad: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    permanent: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    double_sided: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    url: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    octgn_id: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    flavor: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    back_flavor: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    back_text: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    deck_limit: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    health: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    health_per_investigator: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, default=0
    )
    sanity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    skill_willpower: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, default=0
    )
    skill_intellect: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, default=0
    )
    skill_combat: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, default=0
    )
    skill_agility: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True, default=0
    )
    skill_wild: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    real_slot: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    illustrator: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # relationships
    restrictions: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    deck_requirements: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    deck_options: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    customization_text: Mapped[Optional[str]] = mapped_column(
        String(3000), nullable=True
    )
    customization_changes: Mapped[Optional[str]] = mapped_column(
        String(3000), nullable=True
    )
    customization_options: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    imagesrc: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    backimagesrc: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    traits: Mapped[List[TraitModel]] = relationship(
        secondary=card_traits, back_populates="cards", lazy="selectin"
    )

    # Encounter sets relationship
    encounter_sets: Mapped[List["EncounterSetModel"]] = relationship(
        secondary=card_encounter_sets, back_populates="cards", lazy="selectin"
    )
    variants: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    duplicated_by: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    alternated_by: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    taboo_versions: Mapped[List[TabooModel]] = relationship(
        secondary=card_taboos, back_populates="cards"
    )
    encounter_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    encounter_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    encounter_position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    shroud: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    clues: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    victory: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    vengeance: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    doom: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    clues_fixed: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    stage: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    spoilers: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    enemy_damage: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    enemy_evade: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    enemy_fight: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    enemy_horror: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Foreign key for linked card relationship
    linked_to_code: Mapped[Optional[str]] = mapped_column(
        String(50), ForeignKey("cards.code", ondelete="SET NULL"), nullable=True
    )

    # Fixed relationship - this card links TO another card
    linked_card: Mapped[Optional["CardModel"]] = relationship(
        "CardModel",
        foreign_keys=[linked_to_code],
        back_populates="linked_cards",
        remote_side=[code],  # This card is the "parent"
        lazy="noload",  # Prevent lazy loading, must be explicitly loaded
    )

    # Cards that link TO this card
    linked_cards: Mapped[List["CardModel"]] = relationship(
        "CardModel",
        foreign_keys=[linked_to_code],
        back_populates="linked_card",
        lazy="noload",  # Use explicit loading to avoid lazy loading issues
    )

    # Bonded cards relationship
    bonded_cards: Mapped[List["BondedCardModel"]] = relationship(
        "BondedCardModel",
        foreign_keys="BondedCardModel.card_code",
        back_populates="card",
        lazy="noload",  # Use explicit loading to avoid lazy loading issues
    )

    xp: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
