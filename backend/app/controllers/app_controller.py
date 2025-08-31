import json
from fastapi import HTTPException
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
from scoring_model.evaluators.base_evalutor import BaseEvaluator


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
            # Only filter out fields that are handled separately or don't exist in the model
            excluded_fields = {
                "traits",
                "real_traits",
                "linked_card",  # This is a relationship, not a data field
                "linked_cards",  # This is a relationship, not a data field
                "bonded_cards",  # This is a relationship, not a data field
            }

            # Handle linked_to_code specially - only set it if the referenced card exists
            card_dict = {}
            for k, v in card_data.items():
                if (
                    v is not None
                    and k not in excluded_fields
                    and hasattr(CardModel, k)
                    and not k.startswith("_")
                ):
                    if k == "linked_to_code":
                        # Check if the referenced card exists before setting linked_to_code
                        if v:
                            linked_card_exists = await db_session.scalar(
                                select(CardModel).where(CardModel.code == v)
                            )
                            if linked_card_exists:
                                card_dict[k] = v
                            # If linked card doesn't exist, skip this field (will be NULL)
                    else:
                        card_dict[k] = v

            # Create card instance
            card = CardModel(**card_dict)

            # Handle traits separately
            traits_str = str(card_data.get("traits", ""))
            trait_names = [
                name.strip() for name in traits_str.split(".") if name.strip()
            ]

            # Get or create traits using provided session
            for trait_name in trait_names:
                # First try to find existing trait
                trait = await db_session.scalar(
                    select(TraitModel).where(TraitModel.name == trait_name)
                )

                # If trait doesn't exist, create it
                if not trait:
                    trait = TraitModel(name=trait_name)
                    db_session.add(trait)
                    # Flush to get the trait ID for the relationship
                    await db_session.flush()

                # Add trait to card (this will create the relationship in card_traits table)
                card.traits.append(trait)

            # Also handle real_traits if they exist (these might be different from regular traits)
            real_traits_str = str(card_data.get("real_traits", ""))
            if real_traits_str and real_traits_str != traits_str:
                real_trait_names = [
                    name.strip() for name in real_traits_str.split(".") if name.strip()
                ]

                # Get or create real traits using provided session
                for trait_name in real_trait_names:
                    # First try to find existing trait
                    trait = await db_session.scalar(
                        select(TraitModel).where(TraitModel.name == trait_name)
                    )

                    # If trait doesn't exist, create it
                    if not trait:
                        trait = TraitModel(name=trait_name)
                        db_session.add(trait)
                        # Flush to get the trait ID for the relationship
                        await db_session.flush()

                    # Add trait to card if not already present
                    if trait not in card.traits:
                        card.traits.append(trait)

            # Note: Bonded cards will be handled in a separate pass after all cards are created

            return card
        except Exception as e:
            logger.error(f"Error creating card: {e}")
            logger.error(f"Stacktrace: {traceback.format_exc()}")
            raise

    async def _process_bonded_cards(self, raw_cards: List[Dict[str, Any]], db_session) -> None:
        """Second pass: Process bonded card relationships after all cards exist"""
        try:
            from app.models.arkham_model import BondedCardModel
            
            for card_data in raw_cards:
                bonded_cards_data = card_data.get("bonded_cards", [])
                if bonded_cards_data:
                    card_code = card_data.get("code")
                    
                    # Get the card from database
                    card = await db_session.scalar(
                        select(CardModel).where(CardModel.code == card_code)
                    )
                    
                    if card:
                        for bonded_data in bonded_cards_data:
                            if isinstance(bonded_data, dict) and "code" in bonded_data:
                                bonded_card_code = bonded_data["code"]
                                count = bonded_data.get("count", 1)

                                # Check if the bonded card exists
                                bonded_card_exists = await db_session.scalar(
                                    select(CardModel).where(CardModel.code == bonded_card_code)
                                )

                                if bonded_card_exists:
                                    # Check if relationship already exists
                                    existing_relationship = await db_session.scalar(
                                        select(BondedCardModel).where(
                                            BondedCardModel.card_code == card_code,
                                            BondedCardModel.bonded_card_code == bonded_card_code
                                        )
                                    )
                                    
                                    if not existing_relationship:
                                        bonded_relationship = BondedCardModel(
                                            card_code=card_code,
                                            bonded_card_code=bonded_card_code,
                                            count=count,
                                        )
                                        db_session.add(bonded_relationship)
            
            await db_session.commit()
            logger.info("Bonded card relationships processed successfully")
            
        except Exception as e:
            logger.error(f"Error processing bonded cards: {e}")
            logger.error(f"Stacktrace: {traceback.format_exc()}")
            await db_session.rollback()

    async def fetch_cards(self, encounter: int = 0) -> None:
        try:
            raw_cards = await self._arkhamdb_controller.fetch_all_card_data(
                params={"encounter": encounter}
            )
            cards = []

            async with self.db as db:
                it = iter(raw_cards)
                while batch := list(islice(it, self.BATCH_SIZE)):
                    for card_data in batch:
                        # Check if card exists with traits pre-loaded
                        stmt = (
                            select(CardModel)
                            .options(selectinload(CardModel.traits))
                            .where(CardModel.code == card_data.get("code"))
                        )
                        existing_card = await db.execute(stmt)
                        existing_card = existing_card.scalar_one_or_none()

                        if existing_card:
                            # Update existing card fields directly
                            # Use the same filtering logic as _create_card
                            excluded_fields = {
                                "traits",
                                "real_traits",
                                "bonded_cards",  # This is handled separately
                                "linked_card",  # This is a relationship, not a data field
                                "linked_cards",  # This is a relationship, not a data field
                            }

                            # Handle linked_to_code specially - only set it if the referenced card exists
                            card_dict = {}
                            for k, v in card_data.items():
                                if (
                                    v is not None
                                    and k not in excluded_fields
                                    and hasattr(CardModel, k)
                                    and not k.startswith("_")
                                ):
                                    if k == "linked_to_code":
                                        # Check if the referenced card exists before setting linked_to_code
                                        if v:
                                            linked_card_exists = await db.scalar(
                                                select(CardModel).where(
                                                    CardModel.code == v
                                                )
                                            )
                                            if linked_card_exists:
                                                card_dict[k] = v
                                            # If linked card doesn't exist, skip this field (will be NULL)
                                    else:
                                        card_dict[k] = v

                            # Only set simple fields, not relationships or complex data
                            for key, value in card_dict.items():
                                if hasattr(existing_card, key) and not key.startswith(
                                    "_"
                                ):
                                    # For JSON fields, ensure they're properly formatted
                                    if isinstance(value, dict) and key in [
                                        "restrictions",
                                        "deck_requirements",
                                        "deck_options",
                                        "customization_options",
                                        "variants",
                                        "duplicated_by",
                                        "alternated_by",
                                        "bonded_cards",  # Add bonded_cards as JSON field
                                        "real_traits",  # Add real_traits as JSON field
                                    ]:
                                        setattr(existing_card, key, value)
                                    elif not isinstance(value, dict):
                                        setattr(existing_card, key, value)
                                    else:
                                        # Log any unexpected dict fields to debug
                                        logger.warning(
                                            f"Skipping dict field {key} with value {value}"
                                        )

                            # Handle traits for existing cards (update them)
                            traits_str = str(card_data.get("traits", ""))
                            trait_names = [
                                name.strip()
                                for name in traits_str.split(".")
                                if name.strip()
                            ]

                            # Handle traits for existing cards by updating the relationship
                            # First, get all the traits we need to associate
                            all_traits = []

                            # Process regular traits
                            for trait_name in trait_names:
                                # First try to find existing trait
                                trait = await db.scalar(
                                    select(TraitModel).where(
                                        TraitModel.name == trait_name
                                    )
                                )

                                # If trait doesn't exist, create it
                                if not trait:
                                    trait = TraitModel(name=trait_name)
                                    db.add(trait)
                                    # Flush to get the trait ID for the relationship
                                    await db.flush()

                                all_traits.append(trait)

                            # Process real_traits if they exist
                            real_traits_str = str(card_data.get("real_traits", ""))
                            if real_traits_str and real_traits_str != traits_str:
                                real_trait_names = [
                                    name.strip()
                                    for name in real_traits_str.split(".")
                                    if name.strip()
                                ]

                                for trait_name in real_trait_names:
                                    # First try to find existing trait
                                    trait = await db.scalar(
                                        select(TraitModel).where(
                                            TraitModel.name == trait_name
                                        )
                                    )

                                    # If trait doesn't exist, create it
                                    if not trait:
                                        trait = TraitModel(name=trait_name)
                                        db.add(trait)
                                        # Flush to get the trait ID for the relationship
                                        await db.flush()

                                    # Add to all_traits if not already present
                                    if trait not in all_traits:
                                        all_traits.append(trait)

                            # Now set the traits relationship directly
                            existing_card.traits = all_traits

                            cards.append(existing_card)
                        else:
                            # Create new card
                            card = await self._create_card(card_data, db)
                            db.add(card)
                            cards.append(card)

                    await db.commit()

                # Second pass: Handle bonded card relationships
                await self._process_bonded_cards(raw_cards, db)

            # return [card.to_dict() for card in cards]
        except Exception as e:
            logger.error(f"Error fetching cards: {e}")
            logger.error(f"Stacktrace: {traceback.format_exc()}")

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

    async def calculate_card_value(self, card_id: str) -> float:
        try:
            return 0
            # card = await self.card_repo.get_by_id(card_id)
            # return BaseEvaluator.evaluate_card_strength(
            #     card.effects,
            #     card.trigger_probs,
            #     card.pass_probs,
            #     card.investigator_scaling,
            #     card.synergy_range,
            #     card.scenario_weight,
            # )
        except Exception as e:
            logger.error(f"Error calculating card value: {e}")
            logger.error(f"Stacktrace: {traceback.format_exc()}")
            return 0

    async def get_card(self, card_id: str) -> Card:
        async with self.db as db:
            # Try to get from database first
            cardData = await self.card_repo.get_first(
                filters={"filter_by[code][equals]": card_id},
                include=["traits", "linked_card", "bonded_cards"],
                # filters={"code": cardCode}
            )
            if not cardData:
                raise HTTPException(status_code=404, detail="Card not found")
            return Card.from_model(cardData)
