import asyncio
import logging

from app.core.redis_client import redis_client
from app.services.arkhamdb_service import ArkhamDBService
from app.services.deck_service import DeckService

logger = logging.getLogger(__name__)

# Must stay comfortably under DeckService's 24h (86400s) cache TTL for
# `decks_raw:last_{days}_days` so the cache never goes cold under normal
# operation — the endpoint's synchronous fallback path is what produces the
# 502s (cold fetch of a year of ArkhamDB data blows past the gateway's
# request timeout).
WARM_INTERVAL_SECONDS = 20 * 60 * 60  # 20h
WARM_DAYS = 365
_LOCK_KEY = "arkham:lock:warm_bulk_decks"
_LOCK_TTL_SECONDS = 30 * 60  # long enough to cover a slow fetch, short enough to self-heal


async def _try_acquire_lock() -> bool:
    """Best-effort cross-worker lock so only one of the (4) uvicorn workers
    performs the refresh. If Redis is unavailable, returns True so the lone
    in-process warmer still runs (duplicate work across workers is a much
    smaller cost than never warming at all)."""
    if not redis_client.is_connected:
        return True
    try:
        return bool(
            await redis_client.client.set(
                _LOCK_KEY, "1", nx=True, ex=_LOCK_TTL_SECONDS
            )
        )
    except Exception as e:
        logger.warning(f"Cache warmer lock check failed, proceeding anyway: {e}")
        return True


async def warm_bulk_decks_cache_once() -> None:
    if not await _try_acquire_lock():
        logger.info("Cache warmer: another worker holds the lock, skipping")
        return

    logger.info(f"Cache warmer: refreshing {WARM_DAYS}-day deck cache")
    deck_service = DeckService(ArkhamDBService())
    try:
        decks = await deck_service.get_decks_last_n_days(
            WARM_DAYS, force_refresh=True
        )
        logger.info(f"Cache warmer: refreshed {len(decks)} decks")
    except Exception as e:
        logger.error(f"Cache warmer: failed to refresh deck cache: {e}")


async def warm_bulk_decks_cache_loop() -> None:
    """Runs for the lifetime of the app; keeps the shared bulk-decks cache
    warm so no user request ever pays for a cold 365-day ArkhamDB fetch."""
    while True:
        try:
            await warm_bulk_decks_cache_once()
        except Exception as e:
            logger.error(f"Cache warmer loop error: {e}")
        await asyncio.sleep(WARM_INTERVAL_SECONDS)
