from __future__ import annotations
from typing import Any, List, Optional
from app.schemas.base import BaseSchema
from app.models.arkham_model import CardModel
from scoring_model.Card.taboo_version import TabooVersion


class BondedCard(BaseSchema):
    code: str
    count: int


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

    encounter_code: str | None = None
    encounter_name: str | None = None
    encounter_position: int | None = None
    shroud: int | None = None
    clues: int | None = None
    victory: int | None = None
    spoilers: bool | None = None

    linked_card: Card | None = None
    bonded_cards: List[BondedCard] = []

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

    @classmethod
    def _get_linked_card(
        cls, card_model: CardModel, _processed_codes: set[str]
    ) -> Optional["Card"]:
        """Safely get linked card without triggering lazy loading"""
        try:
            # Check if there's a linked_to_code
            if not card_model.linked_to_code:
                return None

            # Try to access linked_card - it should be loaded if included in the query
            linked_card = card_model.linked_card
            if linked_card is not None:
                return cls.from_model(linked_card, _processed_codes)

            return None
        except Exception:
            # If accessing linked_card triggers lazy loading or any other error, return None
            return None

    @classmethod
    def from_model(
        cls, card_model: CardModel, _processed_codes: set[str] | None = None
    ) -> "Card":
        """Convert a database CardModel to a Card schema"""
        if _processed_codes is None:
            _processed_codes = set()

        # Avoid infinite recursion
        if card_model.code in _processed_codes:
            # Return a basic version without linked_card to break recursion
            return cls(
                code=card_model.code,
                name=card_model.name,
                type_name=card_model.type_name,
                faction_name=card_model.faction_name,
                health_per_investigator=bool(card_model.health_per_investigator),
                traits=[],
            )

        _processed_codes.add(card_model.code)

        return cls(
            code=card_model.code,
            name=card_model.name,
            real_name=card_model.real_name,
            subname=card_model.subname,
            cost=card_model.cost,
            text=card_model.text,
            real_text=card_model.real_text,
            type_code=card_model.type_code,
            type_name=card_model.type_name,
            faction_code=card_model.faction_code,
            faction_name=card_model.faction_name,
            alternate_of_code=card_model.alternate_of_code,
            alternate_of_name=card_model.alternate_of_name,
            pack_code=card_model.pack_code,
            pack_name=card_model.pack_name,
            position=card_model.position,
            quantity=card_model.quantity,
            is_unique=card_model.is_unique,
            exceptional=card_model.exceptional,
            myriad=card_model.myriad,
            permanent=card_model.permanent,
            double_sided=card_model.double_sided,
            url=card_model.url,
            flavor=card_model.flavor,
            back_flavor=card_model.back_flavor,
            back_text=card_model.back_text,
            deck_limit=card_model.deck_limit,
            health=card_model.health,
            health_per_investigator=bool(card_model.health_per_investigator),
            sanity=card_model.sanity,
            skill_willpower=card_model.skill_willpower,
            skill_intellect=card_model.skill_intellect,
            skill_combat=card_model.skill_combat,
            skill_agility=card_model.skill_agility,
            skill_wild=card_model.skill_wild,
            real_slot=card_model.real_slot,
            illustrator=card_model.illustrator,
            restrictions=card_model.restrictions,
            deck_requirements=card_model.deck_requirements,
            deck_options=card_model.deck_options,
            imagesrc=card_model.imagesrc,
            backimagesrc=card_model.backimagesrc,
            octgn_id=card_model.octgn_id,
            traits=[Trait(name=trait.name) for trait in (card_model.traits or [])],
            variants=card_model.variants,
            linked_card=cls._get_linked_card(card_model, _processed_codes),
            bonded_cards=[
                BondedCard(code=bonded.bonded_card_code, count=bonded.count)
                for bonded in (card_model.bonded_cards or [])
            ],
        )


class Trait(BaseSchema):
    name: str
    cards: List[Card] = []


class EffectQuantities(BaseSchema):
    actions: Optional[float] = 0
    player_card_draws: Optional[float] = 0
    damage: Optional[float] = 0
    clues: Optional[float] = 0
    skill_icon: Optional[float] = 0
    horror: Optional[float] = 0
    health: Optional[float] = 0
    uses: Optional[int] = 0
    movement: Optional[float] = 0
    doom: Optional[float] = 0
    fast_actions: Optional[float] = 0
    reactions: Optional[float] = 0
    exhaust_costs: Optional[float] = 0
    encounter_card_draw: Optional[int] = 0
    enemy: Optional[float] = 0
    XP: Optional[float] = 0
    special_effect: Optional[float] = 0  # generic boost value
    context: Optional[str] = None


class CardGPTResponse(BaseSchema):
    name: str
    best_case_quantities: EffectQuantities
    typical_case_quantities: EffectQuantities
    worse_case_quantities: EffectQuantities
    notes: str
    have_trigger_prob: bool
    trigger_condition: str
    have_pass_prob: bool
    pass_condition: str
