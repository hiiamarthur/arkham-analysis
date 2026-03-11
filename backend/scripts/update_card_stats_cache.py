#!/usr/bin/env python3
"""
Cron job script to pre-calculate and cache card statistics.

Run this script weekly to update card stats cache:
- Calculates stats for all player cards
- Stores results in Redis with TTL
- Adds last_updated timestamp

Schedule with cron (every Sunday at midnight):
0 0 * * 0 /path/to/python /path/to/backend/scripts/update_card_stats_cache.py

Or use APScheduler for programmatic scheduling.
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.database import get_db
from app.services.card_service import CardService
from app.repositories.base_repository import BaseRepository
from app.models.card_model import CardModel
from app.services.deck_service import DeckService
from app.models.deck_model import DeckModel
from app.core.redis_client import get_redis_client


async def update_card_stats_cache():
    """
    Pre-calculate and cache stats for all player cards.
    """
    print(f"[{datetime.now()}] Starting card stats cache update...")

    # Get database session
    async for db in get_db():
        try:
            # Initialize services
            card_repo = BaseRepository(CardModel, db)
            deck_repo = BaseRepository(DeckModel, db)
            deck_service = DeckService(db, deck_repo)
            card_service = CardService(db, card_repo, deck_service)

            # Get Redis client
            redis_client = await get_redis_client()

            # Get all player cards (not investigators, not encounter cards)
            all_cards = await card_repo.get_all(
                filters={
                    "filter_by[type_code][not_in]": "investigator,scenario,location,enemy,treachery,act,agenda"
                }
            )

            print(f"Found {len(all_cards)} player cards to process...")

            # Track statistics
            success_count = 0
            error_count = 0

            # Cache TTL: 7 days (weekly updates)
            cache_ttl = 60 * 60 * 24 * 7  # 7 days in seconds

            # Calculate next update time (7 days from now)
            next_update = datetime.now() + timedelta(days=7)

            for card in all_cards:
                try:
                    # Calculate stats
                    stats = await card_service.get_card_stats(
                        card.code,
                        days=365,
                        trend_period="month"
                    )

                    # Add metadata
                    stats["cache_metadata"] = {
                        "last_updated": datetime.now().isoformat(),
                        "next_update": next_update.isoformat(),
                        "cache_version": "1.0"
                    }

                    # Store in Redis
                    cache_key = f"card_stats:{card.code}"
                    await redis_client.setex(
                        cache_key,
                        cache_ttl,
                        json.dumps(stats)
                    )

                    success_count += 1

                    if success_count % 50 == 0:
                        print(f"Processed {success_count} cards...")

                except Exception as e:
                    print(f"Error processing card {card.code}: {e}")
                    error_count += 1

            print(f"\n[{datetime.now()}] Cache update complete!")
            print(f"✓ Successfully cached: {success_count} cards")
            print(f"✗ Errors: {error_count} cards")
            print(f"Next update: {next_update.strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:
            print(f"Fatal error during cache update: {e}")
            raise
        finally:
            break  # Exit the async generator


if __name__ == "__main__":
    asyncio.run(update_card_stats_cache())
