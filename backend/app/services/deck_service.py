from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, cast
import asyncio
from collections import defaultdict

from app.services.arkhamdb_service import ArkhamDBService
from app.services.cache_service import cache_service
from app.schemas.card_schema import DeckListSchema


class DeckService:
    """Service for managing deck data with caching and batching"""

    def __init__(self, arkhamdb_service: ArkhamDBService):
        self.arkhamdb_service = arkhamdb_service
        self.cache_service = cache_service

    async def get_decks_last_n_days(
        self,
        days: int,
        batch_size: int = 30,
        max_concurrent: int = 10,
        use_cache: bool = True,
    ) -> List[DeckListSchema]:
        """
        Get all decks from the last N days with caching and batching
        Returns List[DeckListSchema] objects for service consumption
        """
        # Try cache first for any significant request (cache raw data, not schema objects)
        raw_decks = None
        if use_cache and days >= 30:
            try:
                cache_key = f"decks_raw:last_{days}_days"
                cached_result = await self.cache_service.get_with_key(
                    "bulk_decks", cache_key
                )
                if cached_result:
                    print(
                        f"Cache HIT: type={type(cached_result)}, len={len(cached_result) if hasattr(cached_result, '__len__') else 'N/A'}"
                    )
                    # Clear corrupted cache for now and fetch fresh
                    # await self.cache_service.delete_with_key("bulk_decks", cache_key)
                    # print("Cleared corrupted cache, will fetch fresh data")
                    # raw_decks = None
                    raw_decks = [
                        (
                            DeckListSchema.from_json(deck)
                            if isinstance(deck, str)
                            else DeckListSchema.from_dict(deck)
                        )
                        for deck in cached_result
                    ]
                    print(
                        f"Cached decks: type={type(raw_decks)}, len={len(raw_decks) if hasattr(raw_decks, '__len__') else 'N/A'}"
                    )
                    return raw_decks
                else:
                    print("Cache MISS")
            except Exception as e:
                print(f"Cache error (continuing without cache): {e}")
                return []
                # Clear potentially corrupted cache
                try:
                    await self.cache_service.delete_with_key("bulk_decks", cache_key)
                except:
                    pass

        # Fetch deck data if not cached
        if raw_decks is None:
            print(f"Fetching fresh data for {days} days")
            if days > 1000:
                raw_decks = await self._process_large_date_range(
                    days, batch_size, max_concurrent
                )
            else:
                raw_decks = await self._process_small_date_range(days, max_concurrent)

            print(
                f"Fetched raw_decks: type={type(raw_decks)}, len={len(raw_decks) if hasattr(raw_decks, '__len__') else 'N/A'}"
            )

            # Cache the raw data for reuse within the same server session
            if use_cache and days >= 30:
                try:
                    cache_key = f"decks_raw:last_{days}_days"
                    await self.cache_service.set_with_key(
                        "bulk_decks", cache_key, raw_decks, ttl=86400
                    )
                    print(f"Cached raw deck data for {days} days")
                except Exception as e:
                    print(f"Cache set error: {e}")

        # Convert raw dict data to DeckListSchema objects (always do this conversion)
        all_decks = []
        if raw_decks:
            print(f"Converting {len(raw_decks)} raw decks")
            for i, deck_data in enumerate(raw_decks):
                if deck_data and isinstance(deck_data, dict):
                    all_decks.append(self._dict_to_deck_schema(deck_data))
                elif i < 3:  # Only log first few for debugging
                    print(
                        f"Skipping deck {i}: type={type(deck_data)}, is_dict={isinstance(deck_data, dict)}"
                    )
        else:
            print("No raw_decks to convert")

        print(f"Converted to {len(all_decks)} DeckListSchema objects")
        return all_decks

    async def get_decks_by_date_range(
        self, start_date: datetime, end_date: datetime, use_cache: bool = True
    ) -> List[DeckListSchema]:
        """Get decks within a specific date range"""
        days = (end_date - start_date).days + 1
        return await self.get_decks_last_n_days(days, use_cache=use_cache)

    async def get_deck_summary(
        self,
        days: int,
        batch_size: int = 30,
        max_concurrent: int = 10,
        use_cache: bool = True,
    ) -> Dict[str, Any]:

        # Get full deck data
        all_decks = await self.get_decks_last_n_days(
            days, batch_size, max_concurrent, use_cache
        )

        # Create summary
        result = {
            "total_decks": len(all_decks),
            "days_processed": days,
            "batches": (days + batch_size - 1) // batch_size if days > 1000 else 1,
        }

        return result

    async def _process_small_date_range(
        self, days: int, max_concurrent: int
    ) -> List[DeckListSchema]:
        """Process smaller date ranges with simple concurrency"""
        semaphore = asyncio.Semaphore(min(max_concurrent, days))
        current_date = datetime.now()

        tasks = [
            self._fetch_decks_with_semaphore(
                semaphore, (current_date - timedelta(days=i)).strftime("%Y-%m-%d")
            )
            for i in range(days)
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)
        all_decks = []

        for i, result in enumerate(results):
            if isinstance(result, Exception):
                date = (current_date - timedelta(days=i)).strftime("%Y-%m-%d")
                print(f"Failed to fetch decks for {date}: {result}")
                continue
            if result is not None and isinstance(result, list):
                all_decks.extend(result)  # These are raw dicts from API

        return all_decks

    async def _process_large_date_range(
        self, total_days: int, batch_size: int, max_concurrent: int
    ) -> List[DeckListSchema]:
        """Process large date ranges in batches"""
        all_decks = []
        current_date = datetime.now()

        for batch_start in range(0, total_days, batch_size):
            batch_end = min(batch_start + batch_size, total_days)
            batch_days = batch_end - batch_start

            print(
                f"Processing batch: days {batch_start}-{batch_end-1} ({batch_days} days)"
            )

            semaphore = asyncio.Semaphore(min(max_concurrent, batch_days))
            tasks = [
                self._fetch_decks_with_semaphore(
                    semaphore,
                    (current_date - timedelta(days=batch_start + i)).strftime(
                        "%Y-%m-%d"
                    ),
                )
                for i in range(batch_days)
            ]

            batch_results = await asyncio.gather(*tasks, return_exceptions=True)

            for i, result in enumerate(batch_results):
                if isinstance(result, Exception):
                    date = (current_date - timedelta(days=batch_start + i)).strftime(
                        "%Y-%m-%d"
                    )
                    print(f"Failed to fetch decks for {date}: {result}")
                    continue
                if result is not None and isinstance(result, list):
                    all_decks.extend(result)  # These are raw dicts from API

            # Small delay between batches
            if batch_end < total_days:
                await asyncio.sleep(0.5)

        return all_decks

    async def _fetch_decks_with_semaphore(
        self, semaphore: asyncio.Semaphore, date: str
    ):
        """Fetch decks for a date with semaphore rate limiting and retry logic"""
        async with semaphore:
            max_retries = 3
            base_delay = 1.0

            for attempt in range(max_retries):
                try:
                    return await self.arkhamdb_service.fetch_decks_by_date(date)
                except Exception:
                    if attempt == max_retries - 1:
                        raise

                    delay = base_delay * (2**attempt)
                    await asyncio.sleep(delay)
                    continue

    def _dict_to_deck_schema(self, deck_data: dict) -> DeckListSchema:
        """Convert raw dictionary data from ArkhamDB API to DeckListSchema"""
        try:
            # Handle missing or None sideSlots
            side_slots = deck_data.get("sideSlots", {})
            if side_slots is None:
                side_slots = {}

            return DeckListSchema(
                name=deck_data.get("name", ""),
                date_creation=deck_data.get("date_creation", ""),
                date_update=deck_data.get("date_update", ""),
                description_md=deck_data.get("description_md", ""),
                user_id=deck_data.get("user_id", 0),
                investigator_code=deck_data.get("investigator_code", ""),
                investigator_name=deck_data.get("investigator_name", ""),
                slots=deck_data.get("slots", {}),
                sideSlots=side_slots,
                ignoreDeckLimitSlots=deck_data.get("ignoreDeckLimitSlots"),
                version=deck_data.get("version", ""),
                xp=deck_data.get("xp"),
                xp_spent=deck_data.get("xp_spent"),
                xp_adjustment=deck_data.get("xp_adjustment"),
                exile_string=deck_data.get("exile_string"),
                taboo_id=deck_data.get("taboo_id"),
                meta=deck_data.get("meta", ""),
                tags=deck_data.get("tags", ""),
                previous_deck=deck_data.get("previous_deck"),
                next_deck=deck_data.get("next_deck"),
            )
        except Exception as e:
            print(f"Error converting deck data to schema: {e}, data: {deck_data}")
            # Return a minimal valid schema object
            return DeckListSchema(
                name="Unknown",
                date_creation="",
                date_update="",
                description_md="",
                user_id=0,
                investigator_code="",
                investigator_name="",
                slots={},
                sideSlots={},
                ignoreDeckLimitSlots=None,
                version="",
                xp=None,
                xp_spent=None,
                xp_adjustment=None,
                exile_string=None,
                taboo_id=None,
                meta="",
                tags="",
                previous_deck=None,
                next_deck=None,
            )
