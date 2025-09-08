"""
API Layer Card Adapters - Unified conversion logic
Single adapter that maps common fields and determines domain type from type_code
"""

from abc import abstractmethod
from typing import Union, overload, cast
from app.schemas.card_schema import CardSchema
from domain.card import Faction, BaseCard, CardType, PlayerCard, EncounterCard
from domain.card.adapters import register_card_adapter


@register_card_adapter("unified")
class UnifiedCardAdapter:
    """Unified adapter that handles all card types"""

    @abstractmethod
    def schema_to_domain(self, schema: CardSchema) -> BaseCard:
        """Convert schema to appropriate domain object using BaseCard factory"""

        # Create comprehensive card data dictionary with all possible fields
        card_data = {
            # Base card fields (required for all cards)
            "code": schema.code,
            "name": schema.name or "Unknown",
            "card_type": schema.type_code or "unknown",
            "traits": [trait.name for trait in schema.traits] if schema.traits else [],
            "faction": self._map_faction(schema.faction_code),
            "text": schema.text or "",
            "back_text": schema.back_text,
            # Player card fields
            "cost": schema.cost or 0,
            "level": 0,  # Default level
            "skill_willpower": schema.skill_willpower or 0,
            "skill_intellect": schema.skill_intellect or 0,
            "skill_combat": schema.skill_combat or 0,
            "skill_agility": schema.skill_agility or 0,
            "skill_wild": schema.skill_wild or 0,
            "is_unique": schema.is_unique or False,
            "is_permanent": schema.permanent or False,
            "is_exceptional": schema.exceptional or False,
            # Encounter card fields
            "encounter_code": schema.encounter_code or "unknown",
            "health": getattr(schema, "health", None),
            "sanity": getattr(schema, "sanity", None),
            "doom": getattr(schema, "doom", None),
            "clues": getattr(schema, "clues", None),
        }

        # Remove None values to keep the dict clean
        card_data = {k: v for k, v in card_data.items() if v is not None}

        # Dynamically determine the correct factory method based on card type
        card_type = schema.type_code or "unknown"
        try:
            card_type_enum = CardType.from_code(card_type)
            # Get the registered class for this card type
            target_class = BaseCard._registry.get(card_type_enum)
            if target_class:
                return cast(
                    Union[PlayerCard, EncounterCard, BaseCard],
                    target_class.from_dict(card_data),
                )
        except (ValueError, AttributeError):
            pass

        # Fallback to BaseCard factory
        return BaseCard.from_dict(card_data)

    def _map_faction(self, faction_code: str | None) -> Faction:
        """Map faction code to Faction enum"""
        faction_map = {
            "guardian": Faction.GUARDIAN,
            "seeker": Faction.SEEKER,
            "rogue": Faction.ROGUE,
            "mystic": Faction.MYSTIC,
            "survivor": Faction.SURVIVOR,
            "neutral": Faction.NEUTRAL,
            "mythos": Faction.MYTHOS,
        }
        return faction_map.get(faction_code or "neutral", Faction.NEUTRAL)


def initialize_card_adapters():
    """Initialize all card adapters - called at app startup"""
    # Adapter is auto-registered via decorator when this module is imported
    pass
