from __future__ import annotations
from typing import Any, List
from app.schemas.base import BaseSchema
from scoring_model.Card.taboo_version import TabooVersion


class Card(BaseSchema):
    __tablename__ = "cards"
    code: str
    name: str | None = None
    real_name: str | None = None
    subname: str | None = None
    cost: int | None = None
    text: str | None = None
    real_text: str | None = None
    type_code: str | None = None
    type_name: str | None = None
    faction_code: str | None = None
    faction_name: str | None = None
    alternate_of_code: str | None = None
    alternate_of_name: str | None = None
    pack_code: str | None = None
    pack_name: str | None = None
    position: int | None = None
    quantity: int | None = None
    is_unique: bool | None = None
    exceptional: bool | None = None
    myriad: bool | None = None
    permanent: bool | None = None
    double_sided: bool | None = None
    url: str | None = None

    flavor: str | None = None
    back_flavor: str | None = None
    back_text: str | None = None
    deck_limit: int | None = None
    health: int | None = None
    health_per_investigator: bool
    sanity: int | None = None
    skill_willpower: int | None = None
    skill_intellect: int | None = None
    skill_combat: int | None = None
    skill_agility: int | None = None
    skill_wild: int | None = None
    real_slot: str | None = None
    illustrator: str | None = None

    # relationships
    # deck_requirements = relationship(
    #     "DeckRequirement", back_populates="card", uselist=False
    # )
    restrictions: dict | None = None
    deck_requirements: dict | None = None
    deck_options: dict | None = None
    imagesrc: str | None = None
    backimagesrc: str | None = None
    octgn_id: str | None = None
    # deck_options = relationship("DeckOption", back_populates="card")
    traits: List[Trait]
    # images = relationship("CardImage", back_populates="card", uselist=False)
    variants: dict | None = None

    def apply_taboo(self, taboo_version: TabooVersion) -> "Card":
        if taboo_version.cost:
            self.cost = (self.cost or 0) + taboo_version.cost

        if taboo_version.text:
            self.text = (self.text or "") + taboo_version.text

        return self

    def filter_card_for_prompt(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "type_name": self.type_name,
            "faction_name": self.faction_name,
            "cost": self.cost,
            "text": self.text or self.real_text,
            "skill_willpower": self.skill_willpower,
            "skill_intellect": self.skill_intellect,
            "skill_combat": self.skill_combat,
            "skill_agility": self.skill_agility,
            "skill_wild": self.skill_wild,
            "health": self.health,
            "sanity": self.sanity,
        }


class Trait(BaseSchema):
    name: str
    cards: List[Card]
