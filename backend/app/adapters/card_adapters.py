"""
API Layer Card Adapters - Unified conversion logic
Single adapter that maps common fields and determines domain type from type_code
"""

from typing import Union
from app.schemas.card_schema import CardSchema
from domain.card import EncounterCard, PlayerCard, CardType, Faction
from domain.card.adapters import register_card_adapter


@register_card_adapter("unified")
class UnifiedCardAdapter:
    """Unified adapter that handles all card types"""

    def schema_to_domain(self, schema: CardSchema) -> Union[PlayerCard, EncounterCard]:
        """Convert schema to appropriate domain object based on type_code"""

        # Determine if this is a player card or encounter card
        player_card_types = CardType.player_cards
        encounter_card_types = CardType.encounter_cards

        card_type = schema.type_code or "unknown"

        # Extract common fields
        traits = [trait.name for trait in schema.traits] if schema.traits else []
        faction = self._map_faction(schema.faction_code)
        card_type_enum = self._map_card_type(card_type)

        if card_type.lower() in player_card_types:
            return PlayerCard(
                code=schema.code,
                name=schema.name or "Unknown",
                card_type=card_type_enum,
                traits=traits,
                faction=faction,
                text=schema.text or "",
                cost=schema.cost or 0,
                level=0,  # Default level
                skill_willpower=schema.skill_willpower or 0,
                skill_intellect=schema.skill_intellect or 0,
                skill_combat=schema.skill_combat or 0,
                skill_agility=schema.skill_agility or 0,
                skill_wild=schema.skill_wild or 0,
                is_unique=schema.is_unique or False,
                is_permanent=schema.permanent or False,
                is_exceptional=schema.exceptional or False,
            )

        elif card_type.lower() in encounter_card_types:
            return EncounterCard(
                code=schema.code,
                name=schema.name or "Unknown",
                card_type=card_type_enum,
                traits=traits,
                faction=faction,
                text=schema.text or "",
                encounter_code=schema.encounter_code or "unknown",
                back_text=schema.back_text,
            )

        else:
            # Default to encounter card for unknown types
            return EncounterCard(
                code=schema.code,
                name=schema.name or "Unknown",
                card_type=card_type_enum,
                traits=traits,
                faction=faction,
                text=schema.text or "",
                encounter_code=schema.encounter_code or "unknown",
                back_text=schema.back_text,
            )

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

    def _map_card_type(self, type_code: str) -> CardType:
        """Map type code to CardType enum"""
        type_map = {
            "asset": CardType.ASSET,
            "event": CardType.EVENT,
            "skill": CardType.SKILL,
            "investigator": CardType.INVESTIGATOR,
            "enemy": CardType.ENEMY,
            "treachery": CardType.TREACHERY,
            "location": CardType.LOCATION,
            "agenda": CardType.AGENDA,
            "act": CardType.ACT,
            "scenario": CardType.SCENARIO,
        }
        return type_map.get(type_code.lower(), CardType.ASSET)


def initialize_card_adapters():
    """Initialize all card adapters - called at app startup"""
    # Adapter is auto-registered via decorator when this module is imported
    pass
