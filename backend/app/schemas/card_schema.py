from __future__ import annotations
from typing import Any, Dict, List, Optional
from app.schemas.base import BaseSchema
from app.models.arkham_model import CardModel
from domain.Token.token import ChaosToken
from domain.card.taboo_version import TabooVersion


class BondedCardSchema(BaseSchema):
    code: str
    name: str
    count: int


class DeckListSchema(BaseSchema):
    name: str
    date_creation: str
    date_update: str
    description_md: str
    user_id: int
    investigator_code: str
    investigator_name: str
    slots: Dict[str, int]
    sideSlots: Dict[str, int] | List[Any]
    ignoreDeckLimitSlots: Optional[Dict[str, int]]
    version: str
    xp: Optional[int]
    xp_spent: Optional[int]
    xp_adjustment: Optional[int]
    exile_string: Optional[str]
    taboo_id: Optional[int]
    meta: str
    tags: str
    previous_deck: Optional[int]
    next_deck: Optional[int]


class CardSchema(BaseSchema):
    __tablename__ = "cards"
    code: str
    name: str | None = None
    real_name: str | None = None
    subname: str | None = None
    xp: int | None = None
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

    # Investigator-specific stats (populated dynamically for investigator cards)
    average_deck_size: float | None = None
    deck_size_min: int | None = None
    deck_size_max: int | None = None
    meta_share: float | None = None
    total_decks: int | None = None  # Total decks for this investigator
    total_decks_analyzed: int | None = None  # Total decks in meta

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
    traits: List[TraitSchema]
    # images = relationship("CardImage", back_populates="card", uselist=False)
    variants: dict | None = None

    encounter_code: str | None = None
    encounter_name: str | None = None
    encounter_position: int | None = None
    shroud: int | None = None
    clues: int | None = None
    victory: int | None = None
    vengeance: int | None = None
    doom: int | None = None
    clues_fixed: bool | None = None
    stage: int | None = None
    spoilers: bool | None = None

    enemy_damage: int | None = None
    enemy_evade: int | None = None
    enemy_fight: int | None = None
    enemy_horror: int | None = None

    linked_card: CardSchema | None = None
    bonded_cards: List[BondedCardSchema] = []
    related_card: str | None = None

    def apply_taboo(self, taboo_version: TabooVersion) -> "CardSchema":
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
    ) -> Optional["CardSchema"]:
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
    ) -> "CardSchema":
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
            xp=card_model.xp,
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
            deck_options=card_model.deck_options if isinstance(card_model.deck_options, dict) else {},
            imagesrc=card_model.imagesrc,
            backimagesrc=card_model.backimagesrc,
            octgn_id=card_model.octgn_id,
            traits=[
                TraitSchema(name=trait.name) for trait in (card_model.traits or [])
            ],
            variants=card_model.variants,
            encounter_code=card_model.encounter_code,
            encounter_name=card_model.encounter_name,
            encounter_position=card_model.encounter_position,
            shroud=card_model.shroud,
            clues=card_model.clues,
            victory=card_model.victory,
            vengeance=card_model.vengeance,
            doom=card_model.doom,
            clues_fixed=card_model.clues_fixed,
            stage=card_model.stage,
            spoilers=card_model.spoilers,
            enemy_damage=card_model.enemy_damage,
            enemy_evade=card_model.enemy_evade,
            enemy_fight=card_model.enemy_fight,
            enemy_horror=card_model.enemy_horror,
            linked_card=cls._get_linked_card(card_model, _processed_codes),
            related_card=getattr(card_model, '_related_card', None),
            bonded_cards=[
                BondedCardSchema(
                    code=bonded.bonded_card_code,
                    name=bonded.bonded_card.name if bonded.bonded_card and bonded.bonded_card.name else bonded.bonded_card_code,
                    count=bonded.count,
                )
                for bonded in (card_model.bonded_cards or [])
            ],
        )


class TraitSchema(BaseSchema):
    name: str
    cards: List[CardSchema] = []


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


class ScenarioContext(BaseSchema):
    scenario_code: str
    scenario_name: str
    campaign: str
    pack: str
    difficulty: str
    avg_enemy_health: float
    avg_enemy_fight: float
    avg_enemy_evade: float
    elite_enemy_count: int
    enemy_damage_range: List[int]
    enemy_horror_range: List[int]
    primary_enemy_type: str
    location_count: int
    avg_clues_per_location: float
    avg_shroud_value: float
    # locked_doors: bool
    special_movement_rules: bool
    total_clues_in_scenario: int
    chaos_tokens: List[ChaosToken]
    # special_token_effects: Dict[str, Dict[str, str]]
    doom_threshold: int
    agenda_count: int
    act_count: int
    # special_rules: List[str]
    # victory_conditions: str

    # scenario_mechanics: Dict[str, Any]
    encounter_sets: List[str]
    treachery_count: int
    # enemy_spawn_rate: str
    # scenario_length: str
    # resource_scarcity: str
    # card_draw_availability: str
    # action_economy_stress: str
    # tempo: str

    model_config = {"arbitrary_types_allowed": True}


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
