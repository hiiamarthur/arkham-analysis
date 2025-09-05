from typing import List, Optional, Union
from app.models.arkham_model import CardModel
from app.schemas.card_schema import CardSchema
from domain.card import EncounterCard, PlayerCard, CardType, Faction


class CardAdapter:
    """Handles conversions between different card representations"""

    @staticmethod
    def model_to_schema(card_model: CardModel) -> CardSchema:
        """Convert CardModel to CardSchema"""
        return CardSchema.from_model(card_model)

    @staticmethod
    def schema_to_domain(card_schema: CardSchema) -> Union[EncounterCard, PlayerCard]:
        """Convert CardSchema to domain object"""
        if card_schema.type_code in ["enemy", "treachery", "location"]:
            # return EncounterCard(
            #     code=card_schema.code,
            #     name=card_schema.name or "",
            #     card_type=CardType.from_code(card_schema.type_code),
            #     traits=[trait.name for trait in card_schema.traits],
            #     faction=Faction.from_code(card_schema.faction_code),
            #     text=card_schema.text or "",
            #     encounter_code=card_schema.encounter_code or "",
            #     # ... other encounter-specific fields
            # )
        else:
            return PlayerCard(
                code=card_schema.code,
                name=card_schema.name,
                type_code=card_schema.type_code,
                cost=card_schema.cost,
                # ... other player-specific fields
            )

    @staticmethod
    def model_to_domain(card_model: CardModel) -> Union[EncounterCard, PlayerCard]:
        """Direct conversion from model to domain (bypass schema)"""
        schema = CardAdapter.model_to_schema(card_model)
        return CardAdapter.schema_to_domain(schema)

    @staticmethod
    def models_to_domains(
        card_models: List[CardModel],
    ) -> List[Union[EncounterCard, PlayerCard]]:
        """Batch conversion for efficiency"""
        return [CardAdapter.model_to_domain(model) for model in card_models]
