from typing import Any, Dict, List
import httpx
import logging
from app.core.config import settings
from app.services.cache_service import cache_service

logger = logging.getLogger(__name__)

ARKHAMDB_CARDS_URL = settings.ARKHAMDB_URL + "/public/cards/"
ARKHAMDB_TABOOS_URL = settings.ARKHAMDB_URL + "/public/taboos/"


class ArkhamDBService:
    """Service for communicating with ArkhamDB API"""

    def __init__(self):
        self.base_url = settings.ARKHAMDB_URL
        self.timeout = 30.0

    async def fetch_all_card_data(
        self, params: Dict[str, Any] = {}, use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """Fetch card data from ArkhamDB with caching"""
        params = params or {}

        # Try cache first if enabled
        if use_cache:
            cache_key_params = {k: str(v) for k, v in params.items()}
            cached_data = await cache_service.get_with_key(
                "arkhamdb", "cards", **cache_key_params
            )
            if cached_data:
                logger.debug("Cache hit for ArkhamDB cards")
                return cached_data

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(ARKHAMDB_CARDS_URL, params=params)
                response.raise_for_status()
                data = response.json()

                # Cache the result if caching is enabled
                if use_cache:
                    await cache_service.set_with_key(
                        "arkhamdb",
                        "cards",
                        data,
                        ttl=settings.CACHE_TTL_DEFAULT,
                        **cache_key_params,
                    )
                    logger.debug("Cached ArkhamDB cards data")

                return data

        except httpx.HTTPError as e:
            logger.error(
                f"HTTP error fetching cards from ArkhamDB: {e.with_traceback(None)}"
            )
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching cards: {e}")
            raise

    async def fetch_all_taboo_data(
        self, use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """Fetch taboo data from ArkhamDB with caching"""

        # Try cache first if enabled
        if use_cache:
            cached_data = await cache_service.get_with_key("arkhamdb", "taboos")
            if cached_data:
                logger.debug("Cache hit for ArkhamDB taboos")
                return cached_data

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(ARKHAMDB_TABOOS_URL)
                response.raise_for_status()
                data = response.json()

                # Cache the result if caching is enabled
                if use_cache:
                    await cache_service.set_with_key(
                        "arkhamdb",
                        "taboos",
                        data,
                        ttl=settings.CACHE_TTL_DEFAULT * 2,  # Cache taboos longer
                    )
                    logger.debug("Cached ArkhamDB taboos data")

                return data

        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching taboos from ArkhamDB: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching taboos: {e}")
            raise

    async def fetch_card_by_code(
        self, card_code: str, use_cache: bool = True
    ) -> Dict[str, Any]:
        """Fetch a specific card by code"""
        # Try cache first
        if use_cache:
            cached_card = await cache_service.get_with_key(
                "arkhamdb", "card", code=card_code
            )
            if cached_card:
                logger.debug(f"Cache hit for ArkhamDB card: {card_code}")
                return cached_card

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{ARKHAMDB_CARDS_URL}/{card_code}"
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

                # Cache the result
                if use_cache:
                    await cache_service.set_with_key(
                        "arkhamdb",
                        "card",
                        data,
                        ttl=settings.CACHE_TTL_CARDS,
                        code=card_code,
                    )
                    logger.debug(f"Cached ArkhamDB card: {card_code}")

                return data

        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching card {card_code}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching card {card_code}: {e}")
            raise

    async def invalidate_cache(self) -> None:
        """Invalidate all ArkhamDB cache entries"""
        deleted = await cache_service.invalidate_by_pattern("arkhamdb", "*")
        logger.info(f"Invalidated {deleted} ArkhamDB cache entries")

    async def health_check(self) -> Dict[str, Any]:
        """Check if ArkhamDB API is accessible"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(self.base_url)
                return {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "status_code": response.status_code,
                    "response_time_ms": response.elapsed.total_seconds() * 1000,
                }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
