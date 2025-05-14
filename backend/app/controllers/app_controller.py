import json
from sqlalchemy import select, insert, update
from app.controllers.arkhamdb_controller import ArkhamDBController
from app.models.arkham_model import CardModel, TabooModel, TraitModel
from typing import List, Dict, Any
import asyncio
from itertools import islice
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
import traceback
import logging
from sqlalchemy.orm import Session, selectinload


from app.schemas.card_schema import Card
from app.repositories.base_repositories import BaseRepository

logger = logging.getLogger(__name__)


class AppController:
    _instance = None
    _cards_cache: List[CardModel] = []
    BATCH_SIZE = 100  # Process cards in batches

    def __init__(self, db: AsyncSession):
        self.card_repo = BaseRepository(CardModel, db)
        self.db = db
        self._arkhamdb_controller = ArkhamDBController()

    async def _create_card(self, card_data: Dict[str, Any], db_session) -> CardModel:
        try:
            # Filter out None values, traits, and invalid fields
            card_dict = {
                k: v
                for k, v in card_data.items()
                if v is not None
                and k != "traits"
                and k != "real_traits"
                and hasattr(CardModel, k)
            }

            # Create card instance
            card = CardModel(**card_dict)

            # Handle traits separately
            traits_str = str(card_data.get("traits", ""))
            trait_names = [
                name.strip() for name in traits_str.split(".") if name.strip()
            ]

            # Get or create traits using provided session
            for trait_name in trait_names:
                trait = await db_session.scalar(
                    select(TraitModel).where(TraitModel.name == trait_name)
                )
                if trait:
                    card.traits.append(trait)

            return card
        except Exception as e:
            logger.error(f"Error creating card: {e}")
            logger.error(f"Stacktrace: {traceback.format_exc()}")
            raise

    async def get_cards(self) -> List[Dict[str, Any]]:
        try:
            raw_cards = await self._arkhamdb_controller.fetch_all_card_data()
            cards = []

            async with self.db as db:
                it = iter(raw_cards)
                while batch := list(islice(it, self.BATCH_SIZE)):
                    for card_data in batch:
                        # Check if card exists
                        stmt = select(CardModel).where(
                            CardModel.code == card_data.get("code")
                        )
                        existing_card = await db.execute(stmt)
                        existing_card = existing_card.scalar_one_or_none()

                        if existing_card:
                            # Update existing card fields directly
                            card_dict = {
                                k: v
                                for k, v in card_data.items()
                                if v is not None
                                and k != "traits"
                                and hasattr(CardModel, k)
                            }
                            for key, value in card_dict.items():
                                setattr(existing_card, key, value)
                            cards.append(existing_card)
                        else:
                            # Create new card
                            card = await self._create_card(card_data, db)
                            db.add(card)
                            cards.append(card)

                    await db.commit()

            return [card.to_dict() for card in cards]
        except Exception as e:
            logger.error(f"Error fetching cards: {e}")
            logger.error(f"Stacktrace: {traceback.format_exc()}")
            return []

    async def get_taboos(self) -> List[Dict[str, Any]]:
        try:
            raw_taboos = await self._arkhamdb_controller.fetch_all_taboo_data()
            taboos = []

            async with self.db as db:
                for taboo_data in raw_taboos:
                    cards = json.loads(taboo_data.get("cards", "[]"))
                    for card in cards:
                        stmt = (
                            select(CardModel)
                            .options(selectinload(CardModel.taboo_versions))
                            .where(CardModel.code == card.get("code"))
                        )
                        existing_card = await db.execute(stmt)
                        existing_card = existing_card.scalar_one_or_none()

                        if existing_card:
                            taboo = TabooModel(
                                text=card.get("text"),
                                cost=card.get("cost"),
                                level=card.get("xp"),
                                code=card.get("code"),
                                taboo_code=taboo_data.get("code"),
                            )
                            existing_card.taboo_versions.append(taboo)
                            db.add(taboo)
                            taboos.append(taboo.to_dict())

                await db.commit()
            return taboos
        except Exception as e:
            logger.error(f"Error fetching taboos: {e}")
            logger.error(f"Stacktrace: {traceback.format_exc()}")
            return []

    # async def get_card(self, card_id: str) -> Card:
    #     async with SessionLocal() as db:
    #         # Try to get from database first
    #         card = await db.execute(select(Card).filter(Card.code == card_id))
    #         card = card.scalar_one_or_none()

    #         if not card:
    #             # If not in database, fetch from API
    #             raw_card = await self._arkhamdb_controller.get_card(card_id)
    #             if raw_card:
    #                 card = self._create_card(raw_card)
    #                 db.add(card)
    #                 await db.commit()

    #         return card
