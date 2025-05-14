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
    text: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    real_text: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    type_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    type_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    faction_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    faction_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
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
    octgn_id: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    flavor: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    back_flavor: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    back_text: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
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
        String(1000), nullable=True
    )
    customization_changes: Mapped[Optional[str]] = mapped_column(
        String(1000), nullable=True
    )
    customization_options: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    imagesrc: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    backimagesrc: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    traits: Mapped[List[TraitModel]] = relationship(
        secondary=card_traits, back_populates="cards"
    )
    variants: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON)
    duplicated_by: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    alternated_by: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    taboo_versions: Mapped[List[TabooModel]] = relationship(
        secondary=card_taboos, back_populates="cards"
    )
