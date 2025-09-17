from typing import Optional, List, cast
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.arkham_model import CardModel
from app.repositories.base_repositories import BaseRepository
from app.services.deck_service import DeckService
from app.adapters.card_adapters import UnifiedCardAdapter
from app.schemas.card_schema import CardSchema
from domain.card.investigator_card import InvestigatorCard
from domain.card.context import InvestigatorStats
from domain.card.card_type import CardType
from domain.card import PlayerCard
from domain.card.deck import Deck
from domain.card.context.card_stats import CardStats


class CardService:
    def __init__(
        self,
        db: AsyncSession,
        card_repo: Optional[BaseRepository[CardModel]],
        deck_service: Optional[DeckService] = None,
    ):
        self.db = db
        self.card_repo = card_repo or BaseRepository(CardModel, db)
        self.deck_service = deck_service

    async def get_card_stats(
        self, card_id: str, days: int = 365, trend_period: str = "month"
    ):
        """Get comprehensive card statistics including popularity and trends"""
        # Get card from database
        card = await self.card_repo.get_first(
            filters={"filter_by[code][equals]": card_id}
        )
        if not card:
            raise ValueError(f"Card with ID {card_id} not found")

        # Get recent deck data if deck_service is available
        decks = []
        if self.deck_service:
            try:
                # Get actual deck objects (not summary) for analysis
                decks = await self.deck_service.get_decks_last_n_days(days)
            except Exception as e:
                print(f"Warning: Could not fetch deck data for card stats: {e}")
        adapter = UnifiedCardAdapter()
        # Create CardStats with the deck data

        # Debug: Check what we actually have
        if decks:
            print("First deck type:", type(decks[0]))
            print("First deck has name:", hasattr(decks[0], "name"))
            if hasattr(decks[0], "name"):
                print("First deck name:", decks[0].name)

        # Convert decks to domain objects
        converted_decks = []
        for deck in decks:
            if hasattr(deck, "name") and deck.name:
                try:
                    converted_deck = Deck.from_dict(
                        {
                            "name": deck.name,
                            "date_creation": getattr(deck, "date_creation", ""),
                            "date_update": getattr(deck, "date_update", ""),
                            "investigator_code": getattr(deck, "investigator_code", ""),
                            "investigator_name": getattr(deck, "investigator_name", ""),
                            "slots": getattr(deck, "slots", {}),
                            "sideSlots": (
                                getattr(deck, "sideSlots", {})
                                if isinstance(getattr(deck, "sideSlots", {}), dict)
                                else {}
                            ),
                            "ignoreDeckLimitSlots": getattr(
                                deck, "ignoreDeckLimitSlots", None
                            ),
                            "xp_spent": getattr(deck, "xp_spent", None),
                            "xp_adjustment": getattr(deck, "xp_adjustment", None),
                            "exile_string": getattr(deck, "exile_string", None),
                            "taboo_id": getattr(deck, "taboo_id", None),
                            "meta": getattr(deck, "meta", ""),
                            "tags": getattr(deck, "tags", ""),
                            "previous_deck": getattr(deck, "previous_deck", None),
                            "next_deck": getattr(deck, "next_deck", None),
                        }
                    )
                    converted_decks.append(converted_deck)
                except Exception as e:
                    print(f"Error converting deck: {e}")

        print("Converted decks:", len(converted_decks))

        card_stats = CardStats(
            cast(
                PlayerCard,
                adapter.schema_to_domain(schema=CardSchema.from_model(card)),
            ),
            converted_decks,
        )

        return {
            "card_info": {"code": card.code, "name": card.name, "type": card.type_name},
            "deck_stats": card_stats.get_deck_stats(trend_period=trend_period),
            "data_source": {
                "decks_analyzed": len(decks),
                "days_covered": days,
                "trend_period": trend_period,
            },
        }

    async def get_investigator_stats(self, investigator_code: str, days: int = 365):
        """Get stats for an investigator"""
        investigator = await self.card_repo.get_first(
            filters={"filter_by[code][equals]": investigator_code}
        )
        print(
            "investigator is",
            investigator.type_code if investigator else "none",
            (investigator.type_code if investigator else "none")
            == CardType.INVESTIGATOR.value,
            investigator_code,
        )
        if not investigator or investigator.type_code != CardType.INVESTIGATOR.value:
            raise ValueError(f"Investigator with ID {investigator_code} not found")

        decks = []
        if self.deck_service:
            try:
                # Get actual deck objects (not summary) for analysis
                decks = await self.deck_service.get_decks_last_n_days(days)
            except Exception as e:
                print(f"Warning: Could not fetch deck data for card stats: {e}")
        adapter = UnifiedCardAdapter()
        # Create CardStats with the deck data

        # Debug: Check what we actually have
        if decks:
            print("First deck type:", type(decks[0]))
            print("First deck has name:", hasattr(decks[0], "name"))
            if hasattr(decks[0], "name"):
                print("First deck name:", decks[0].name)

        # Convert decks to domain objects
        converted_decks = []
        for deck in decks:
            if hasattr(deck, "name") and deck.name:
                try:
                    converted_deck = Deck.from_dict(
                        {
                            "name": deck.name,
                            "date_creation": getattr(deck, "date_creation", ""),
                            "date_update": getattr(deck, "date_update", ""),
                            "investigator_code": getattr(deck, "investigator_code", ""),
                            "investigator_name": getattr(deck, "investigator_name", ""),
                            "slots": getattr(deck, "slots", {}),
                            "sideSlots": (
                                getattr(deck, "sideSlots", {})
                                if isinstance(getattr(deck, "sideSlots", {}), dict)
                                else {}
                            ),
                            "ignoreDeckLimitSlots": getattr(
                                deck, "ignoreDeckLimitSlots", None
                            ),
                            "xp_spent": getattr(deck, "xp_spent", None),
                            "xp_adjustment": getattr(deck, "xp_adjustment", None),
                            "exile_string": getattr(deck, "exile_string", None),
                            "taboo_id": getattr(deck, "taboo_id", None),
                            "meta": getattr(deck, "meta", ""),
                            "tags": getattr(deck, "tags", ""),
                            "previous_deck": getattr(deck, "previous_deck", None),
                            "next_deck": getattr(deck, "next_deck", None),
                        }
                    )
                    converted_decks.append(converted_deck)
                except Exception as e:
                    print(f"Error converting deck: {e}")

        investigator_stats = InvestigatorStats(
            cast(
                InvestigatorCard,
                adapter.schema_to_domain(schema=CardSchema.from_model(investigator)),
            ),
            converted_decks,
        )
        return investigator_stats.get_stats()
