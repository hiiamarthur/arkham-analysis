import json
from fastapi import HTTPException
from sqlalchemy import select, insert, update
from app.services.arkhamdb_service import ArkhamDBService
from app.models.arkham_model import CardModel, TabooModel, TraitModel, EncounterSetModel
from typing import List, Dict, Any, Optional, Union
import asyncio
from itertools import islice
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
import traceback
import logging
from sqlalchemy.orm import Session, selectinload
from app.core.config import settings
from app.schemas.card_schema import CardSchema
from app.repositories.base_repositories import BaseRepository
from app.services.cache_service import cache_service
from domain.card.adapters import card_adapter_registry

logger = logging.getLogger(__name__)


class AppService:
    """Service layer for business logic and data operations"""

    def __init__(
        self,
        db: AsyncSession,
        card_repo: Optional[BaseRepository[CardModel]] = None,
        taboo_repo: Optional[BaseRepository[TabooModel]] = None,
        trait_repo: Optional[BaseRepository[TraitModel]] = None,
        encounter_set_repo: Optional[BaseRepository[EncounterSetModel]] = None,
    ):
        self.db = db
        self.arkhamdb_service = ArkhamDBService()

        # Use injected repositories or create new ones (backwards compatibility)
        self.card_repo = card_repo or BaseRepository(CardModel, db)
        self.taboo_repo = taboo_repo or BaseRepository(TabooModel, db)
        self.trait_repo = trait_repo or BaseRepository(TraitModel, db)
        self.encounter_set_repo = encounter_set_repo or BaseRepository(
            EncounterSetModel, db
        )

        # Batch processing settings
        self.BATCH_SIZE = 100

    async def _create_card(self, card_data: Dict[str, Any], db_session) -> CardModel:
        """Create a new card with traits and relationships"""
        try:
            # Filter out None values, traits, encounter_sets, and invalid fields
            excluded_fields = {
                "traits",
                "real_traits",
                "encounter_set",
                "encounter_sets",
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

            # Handle encounter sets separately (similar to traits)
            encounter_set_code = card_data.get("encounter_set")
            if encounter_set_code:
                # Find or create encounter set
                encounter_set = await db_session.scalar(
                    select(EncounterSetModel).where(
                        EncounterSetModel.code == encounter_set_code
                    )
                )

                # If encounter set doesn't exist, create it
                if not encounter_set:
                    encounter_set = EncounterSetModel(
                        code=encounter_set_code,
                        name=encounter_set_code.replace(
                            "_", " "
                        ).title(),  # Basic name formatting
                        pack_code=card_data.get("pack_code"),
                        pack_name=card_data.get("pack_name"),
                    )
                    db_session.add(encounter_set)
                    # Flush to get the encounter set ID for the relationship
                    await db_session.flush()

                # Add encounter set to card
                card.encounter_sets.append(encounter_set)

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

    async def fetch_cards(self, encounter: int = 0) -> List[CardSchema]:
        """Fetch and sync cards from ArkhamDB"""
        # Invalidate related cache entries before fetching new data
        await cache_service.invalidate_by_tags(
            "card", "cards", "traits", "encounter_sets"
        )

        try:
            raw_cards = await self.arkhamdb_service.fetch_all_card_data(
                params={"encounter": encounter}, use_cache=False
            )
            cards = []

            async with self.db as db:
                it = iter(raw_cards)
                while batch := list(islice(it, self.BATCH_SIZE)):
                    for card_data in batch:
                        # Check if card exists with traits and encounter_sets pre-loaded
                        stmt = (
                            select(CardModel)
                            .options(
                                selectinload(CardModel.traits),
                                selectinload(CardModel.encounter_sets),
                            )
                            .where(CardModel.code == card_data.get("code"))
                        )
                        existing_card = await db.execute(stmt)
                        existing_card = existing_card.scalar_one_or_none()

                        if existing_card:
                            excluded_fields = {
                                "traits",
                                "real_traits",
                                "encounter_set",
                                "encounter_sets",
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

                            # Handle encounter sets for existing cards (similar to traits)
                            encounter_set_code = card_data.get("encounter_code")
                            if encounter_set_code:
                                # Find or create encounter set
                                encounter_set = await db.scalar(
                                    select(EncounterSetModel).where(
                                        EncounterSetModel.code == encounter_set_code
                                    )
                                )

                                # If encounter set doesn't exist, create it
                                if not encounter_set:
                                    encounter_set = EncounterSetModel(
                                        code=encounter_set_code,
                                        name=card_data.get(
                                            "encounter_name"
                                        ),  # Basic name formatting
                                        pack_code=card_data.get("pack_code"),
                                        pack_name=card_data.get("pack_name"),
                                    )
                                    db.add(encounter_set)
                                    # Flush to get the encounter set ID for the relationship
                                    await db.flush()

                                # Update encounter sets relationship
                                # Check if the encounter set is already associated with the card
                                if encounter_set not in existing_card.encounter_sets:
                                    existing_card.encounter_sets.append(encounter_set)

                            cards.append(existing_card)
                        else:
                            # Create new card
                            card = await self._create_card(card_data, db)
                            db.add(card)
                            cards.append(card)

                    await db.commit()

                # Second pass: Handle bonded card relationships
                await self._process_bonded_cards(raw_cards, db)

            # Return empty list since cards are too long to return
            # The cards have been processed and stored in the database
            logger.info(f"Successfully processed {len(cards)} cards")
            return []

        except Exception as e:
            logger.error(f"Error fetching cards: {e}")
            logger.error(f"Stacktrace: {traceback.format_exc()}")
            return []

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
            await cache_service.set_with_key(
                "taboos", "all", taboos, ttl=settings.CACHE_TTL_DEFAULT
            )
            logger.debug("Cached taboos")

            return taboos

        except Exception as e:
            logger.error(f"Error fetching taboos: {e}")
            logger.error(f"Stacktrace: {traceback.format_exc()}")
            return []

    async def get_card(self, card_id: str) -> CardSchema:
        """Get a single card by ID with caching"""
        # Try cache first
        cached_card = await cache_service.get_with_key(
            "card",
            card_id,
            include=["traits", "encounter_sets", "linked_card", "bonded_cards"],
        )
        if cached_card:
            logger.debug(f"Cache hit for card: {card_id}")
            return CardSchema.model_validate(cached_card)

        # Get from database via repository
        cardData = await self.card_repo.get_first(
            filters={"filter_by[code][equals]": card_id},
            include=[
                "traits",
                "encounter_sets",
                "linked_card",
                "bonded_cards.bonded_card",
            ],
        )

        if not cardData:
            # Card not in local DB — fetch from ArkhamDB and seed it on-demand
            try:
                raw = await self.arkhamdb_service.fetch_card_by_code(card_id)
                await self._create_card(raw, self.db)
                await self.db.commit()
                # Re-fetch from DB to get full relationships
                cardData = await self.card_repo.get_first(
                    filters={"filter_by[code][equals]": card_id},
                    include=[
                        "traits",
                        "encounter_sets",
                        "linked_card",
                        "bonded_cards.bonded_card",
                    ],
                )
            except Exception as e:
                logger.warning(f"Could not fetch card {card_id} from ArkhamDB: {e}")

        if not cardData:
            raise HTTPException(status_code=404, detail="Card not found")

        card = CardSchema.from_model(cardData)

        # Cache the result with TTL
        await cache_service.set_with_key(
            "card",
            card_id,
            card.model_dump(),
            ttl=settings.CACHE_TTL_CARDS,
            include=["traits", "encounter_sets", "linked_card", "bonded_cards"],
        )
        logger.debug(f"Cached card: {card_id}")

        return card

    async def get_cards_by_encounter(
        self, encounter: int, limit: int = 100
    ) -> List[CardSchema]:
        """Get cards by encounter with caching"""
        # Try cache first
        cached_cards = await cache_service.get_with_key(
            "cards", "encounter", encounter=encounter, limit=limit
        )
        if cached_cards:
            logger.debug(f"Cache hit for cards encounter={encounter}")
            return [CardSchema.model_validate(card) for card in cached_cards]

        # Get from database
        cards = await self.card_repo.get_all(
            filter_by={"filter_by[encounter][equals]": encounter},
            items_per_page=limit,
            include=["traits", "encounter_sets", "linked_card"],
        )

        if not cards:
            return []

        card_objects = [CardSchema.from_model(card) for card in cards]

        # Cache the results
        await cache_service.set_with_key(
            "cards",
            "encounter",
            [card.model_dump() for card in card_objects],
            ttl=settings.CACHE_TTL_CARDS,
            encounter=encounter,
            limit=limit,
        )
        logger.debug(f"Cached cards for encounter={encounter}")

        return card_objects

    def schema_to_domain(self, card_schema: CardSchema):
        """Convert CardSchema to appropriate domain object using registry"""
        # Use the unified adapter for all cards
        return card_adapter_registry.convert_to_domain("unified", card_schema)
    
    def batch_schema_to_domain(self, card_schemas: List[CardSchema]):
        """Convert multiple CardSchema objects to domain objects"""
        domain_cards = []
        
        for schema in card_schemas:
            try:
                domain_card = self.schema_to_domain(schema)
                domain_cards.append(domain_card)
            except ValueError as e:
                logger.warning(f"Skipping unsupported card {schema.code}: {e}")
                continue
        
        return domain_cards

    async def search_cards(
        self, query: str, page: int = 1, limit: int = 20
    ) -> Dict[str, Any]:
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
            include=["traits", "encounter_sets"],
        )

        results = {
            "cards": [CardSchema.from_model(card).model_dump() for card in cards],
            "total": len(cards),
            "page": page,
            "limit": limit,
        }

        # Cache search results for shorter time
        await cache_service.set_with_key(
            "search",
            "cards",
            results,
            ttl=300,  # 5 minutes
            query=query,
            page=page,
            limit=limit,
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

    async def get_encounter_set_repository(self) -> BaseRepository[EncounterSetModel]:
        """Get encounter set repository for direct database access"""
        return self.encounter_set_repo

    # Service-to-service communication methods
    async def sync_with_arkhamdb(self) -> Dict[str, Any]:
        """Comprehensive sync with ArkhamDB - demonstrates service coordination"""

        # Step 1: Check ArkhamDB health
        health_status = await self.arkhamdb_service.health_check()
        if health_status["status"] != "healthy":
            logger.warning(f"ArkhamDB unhealthy: {health_status}")
            return {
                "status": "failed",
                "reason": "ArkhamDB unavailable",
                "health": health_status,
            }

        # Step 2: Invalidate relevant caches
        await cache_service.invalidate_by_tags(
            "card", "cards", "traits", "taboos", "arkhamdb"
        )

        # Step 3: Fetch fresh data from ArkhamDB service
        try:
            cards_data = await self.arkhamdb_service.fetch_all_card_data(
                use_cache=False
            )
            taboos_data = await self.arkhamdb_service.fetch_all_taboo_data(
                use_cache=False
            )

            # Step 4: Process data through our business logic
            await self.fetch_cards(encounter=0)  # Process all encounters
            taboos = await self.get_taboos()

            return {
                "status": "success",
                "cards_fetched": len(cards_data),
                "taboos_processed": len(taboos),
                "arkhamdb_health": health_status,
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
            external_card = await self.arkhamdb_service.fetch_card_by_code(
                card_code, use_cache=False
            )
        except Exception as e:
            external_card = {"error": str(e)}

        return {
            "local_data": local_card.model_dump() if local_card else None,
            "external_data": external_card,
            "data_sync_needed": local_card is None or "error" in external_card,
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
            "analysis_timestamp": "2025-01-01",  # In real app, use datetime
        }

        await cache_service.set_with_key(
            "analysis", "popularity", analysis_data, ttl=3600, encounter=encounter
        )

        return analysis_data
