import json
from fastapi import HTTPException
from sqlalchemy import select, insert, update
from app.services.arkhamdb_service import ArkhamDBService
from app.models.arkham_model import CardModel, TabooModel, TraitModel
from typing import List, Dict, Any, Optional
import asyncio
from itertools import islice
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
import traceback
import logging
from sqlalchemy.orm import Session, selectinload
from app.core.config import settings
from app.schemas.card_schema import Card
from app.repositories.base_repositories import BaseRepository
from app.services.cache_service import cache_service

logger = logging.getLogger(__name__)


class AppService:
    """Service layer for business logic and data operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.arkhamdb_service = ArkhamDBService()
        
        # Initialize repositories
        self.card_repo = BaseRepository(CardModel, db)
        self.taboo_repo = BaseRepository(TabooModel, db) 
        self.trait_repo = BaseRepository(TraitModel, db)
        
        # Batch processing settings
        self.BATCH_SIZE = 100

    async def _create_card(self, card_data: Dict[str, Any], db_session) -> CardModel:
        """Create a new card with traits and relationships"""
        try:
            # Filter out None values, traits, and invalid fields
            excluded_fields = {
                "traits",
                "real_traits", 
                "linked_card",
                "linked_cards",
                "bonded_cards",
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

            # Also handle real_traits if they exist
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

            return card
            
        except Exception as e:
            logger.error(f"Error creating card: {e}")
            logger.error(f"Stacktrace: {traceback.format_exc()}")
            raise

    async def _process_bonded_cards(
        self, raw_cards: List[Dict[str, Any]], db_session
    ) -> None:
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
                                    select(CardModel).where(
                                        CardModel.code == bonded_card_code
                                    )
                                )

                                if bonded_card_exists:
                                    # Check if relationship already exists
                                    existing_relationship = await db_session.scalar(
                                        select(BondedCardModel).where(
                                            BondedCardModel.card_code == card_code,
                                            BondedCardModel.bonded_card_code
                                            == bonded_card_code,
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
        """Fetch and sync cards from ArkhamDB"""
        # Invalidate related cache entries before fetching new data
        await cache_service.invalidate_by_tags("card", "cards", "traits")
        
        try:
            raw_cards = await self.arkhamdb_service.fetch_all_card_data(
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
                            # Update existing card logic (simplified for brevity)
                            # You would include the full update logic here
                            cards.append(existing_card)
                        else:
                            # Create new card
                            card = await self._create_card(card_data, db)
                            db.add(card)
                            cards.append(card)

                    await db.commit()

                # Second pass: Handle bonded card relationships
                await self._process_bonded_cards(raw_cards, db)

        except Exception as e:
            logger.error(f"Error fetching cards: {e}")
            logger.error(f"Stacktrace: {traceback.format_exc()}")

    async def get_taboos(self) -> List[Dict[str, Any]]:
        """Get taboo data from ArkhamDB"""
        # Try cache first
        cached_taboos = await cache_service.get_with_key("taboos", "all")
        if cached_taboos:
            logger.debug("Cache hit for taboos")
            return cached_taboos

        try:
            raw_taboos = await self.arkhamdb_service.fetch_all_taboo_data()
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

            # Cache the result
            await cache_service.set_with_key("taboos", "all", taboos, ttl=settings.CACHE_TTL_DEFAULT)
            logger.debug("Cached taboos")

            return taboos
            
        except Exception as e:
            logger.error(f"Error fetching taboos: {e}")
            logger.error(f"Stacktrace: {traceback.format_exc()}")
            return []

    async def get_card(self, card_id: str) -> Card:
        """Get a single card by ID with caching"""
        # Try cache first
        cached_card = await cache_service.get_with_key(
            "card", card_id, include=["traits", "linked_card", "bonded_cards"]
        )
        if cached_card:
            logger.debug(f"Cache hit for card: {card_id}")
            return Card.model_validate(cached_card)

        # Get from database via repository
        cardData = await self.card_repo.get_first(
            filters={"filter_by[code][equals]": card_id},
            include=["traits", "linked_card", "bonded_cards.bonded_card"],
        )
        
        if not cardData:
            raise HTTPException(status_code=404, detail="Card not found")

        card = Card.from_model(cardData)

        # Cache the result with TTL
        await cache_service.set_with_key(
            "card",
            card_id,
            card.model_dump(),
            ttl=settings.CACHE_TTL_CARDS,
            include=["traits", "linked_card", "bonded_cards"],
        )
        logger.debug(f"Cached card: {card_id}")

        return card

    async def get_cards_by_encounter(self, encounter: int, limit: int = 100) -> List[Card]:
        """Get cards by encounter with caching"""
        # Try cache first
        cached_cards = await cache_service.get_with_key("cards", "encounter", encounter=encounter, limit=limit)
        if cached_cards:
            logger.debug(f"Cache hit for cards encounter={encounter}")
            return [Card.model_validate(card) for card in cached_cards]

        # Get from database
        cards = await self.card_repo.get_all(
            filter_by={"filter_by[encounter][equals]": encounter},
            items_per_page=limit,
            select_list=["traits", "linked_card"]
        )

        if not cards:
            return []

        card_objects = [Card.from_model(card) for card in cards]
        
        # Cache the results
        await cache_service.set_with_key(
            "cards", "encounter", 
            [card.model_dump() for card in card_objects],
            ttl=settings.CACHE_TTL_CARDS,
            encounter=encounter, limit=limit
        )
        logger.debug(f"Cached cards for encounter={encounter}")

        return card_objects

    async def search_cards(self, query: str, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """Search cards with caching"""
        # Try cache first
        cached_results = await cache_service.get_with_key(
            "search", "cards", query=query, page=page, limit=limit
        )
        if cached_results:
            logger.debug(f"Cache hit for search query='{query}'")
            return cached_results

        # Perform search (simplified example)
        cards = await self.card_repo.get_all(
            filter_by={"filter_by[name][contains]": query},
            page=page,
            items_per_page=limit,
            select_list=["traits"]
        )

        results = {
            "cards": [Card.from_model(card).model_dump() for card in cards],
            "total": len(cards),
            "page": page,
            "limit": limit
        }

        # Cache search results for shorter time
        await cache_service.set_with_key(
            "search", "cards", results, ttl=300,  # 5 minutes
            query=query, page=page, limit=limit
        )
        logger.debug(f"Cached search results for query='{query}'")

        return results

    async def calculate_card_value(self, card_id: str) -> float:
        """Calculate card value (placeholder implementation)"""
        try:
            return 0.0
        except Exception as e:
            logger.error(f"Error calculating card value: {e}")
            return 0.0

    # Repository access methods
    async def get_card_repository(self) -> BaseRepository[CardModel]:
        """Get card repository for direct database access"""
        return self.card_repo
    
    async def get_taboo_repository(self) -> BaseRepository[TabooModel]:
        """Get taboo repository for direct database access"""
        return self.taboo_repo
    
    async def get_trait_repository(self) -> BaseRepository[TraitModel]:
        """Get trait repository for direct database access"""
        return self.trait_repo

    # Service-to-service communication methods
    async def sync_with_arkhamdb(self) -> Dict[str, Any]:
        """Comprehensive sync with ArkhamDB - demonstrates service coordination"""
        
        # Step 1: Check ArkhamDB health
        health_status = await self.arkhamdb_service.health_check()
        if health_status["status"] != "healthy":
            logger.warning(f"ArkhamDB unhealthy: {health_status}")
            return {"status": "failed", "reason": "ArkhamDB unavailable", "health": health_status}

        # Step 2: Invalidate relevant caches
        await cache_service.invalidate_by_tags("card", "cards", "traits", "taboos", "arkhamdb")
        
        # Step 3: Fetch fresh data from ArkhamDB service
        try:
            cards_data = await self.arkhamdb_service.fetch_all_card_data(use_cache=False)
            taboos_data = await self.arkhamdb_service.fetch_all_taboo_data(use_cache=False)
            
            # Step 4: Process data through our business logic
            await self.fetch_cards(encounter=0)  # Process all encounters
            taboos = await self.get_taboos()
            
            return {
                "status": "success",
                "cards_fetched": len(cards_data),
                "taboos_processed": len(taboos),
                "arkhamdb_health": health_status
            }
            
        except Exception as e:
            logger.error(f"Sync failed: {e}")
            return {"status": "failed", "error": str(e)}

    async def get_card_with_external_data(self, card_code: str) -> Dict[str, Any]:
        """Get card with fresh external data - service coordination example"""
        
        # Get local card data
        try:
            local_card = await self.get_card(card_code)
        except HTTPException:
            local_card = None
        
        # Get fresh data from ArkhamDB
        try:
            external_card = await self.arkhamdb_service.fetch_card_by_code(card_code, use_cache=False)
        except Exception as e:
            external_card = {"error": str(e)}
        
        return {
            "local_data": local_card.model_dump() if local_card else None,
            "external_data": external_card,
            "data_sync_needed": local_card is None or "error" in external_card
        }

    # Service composition example
    async def analyze_card_popularity(self, encounter: int) -> Dict[str, Any]:
        """Complex business logic using multiple services"""
        
        # 1. Get cards from database via repository
        cards = await self.get_cards_by_encounter(encounter, limit=1000)
        
        # 2. Get fresh external data for comparison
        external_cards = await self.arkhamdb_service.fetch_all_card_data(
            params={"encounter": encounter}, use_cache=True
        )
        
        # 3. Cache intermediate results
        analysis_data = {
            "local_cards": len(cards),
            "external_cards": len(external_cards),
            "encounter": encounter,
            "analysis_timestamp": "2025-01-01"  # In real app, use datetime
        }
        
        await cache_service.set_with_key(
            "analysis", "popularity", analysis_data, ttl=3600, encounter=encounter
        )
        
        return analysis_data