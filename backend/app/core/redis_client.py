import json
import logging
from typing import Any, Optional, Dict
import redis.asyncio as redis
from app.core.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    _instance: Optional["RedisClient"] = None
    _redis_client: Optional[redis.Redis] = None
    _connected: bool = False
    _connect_attempted: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def connect(self) -> None:
        """Initialize Redis connection. Redis is optional — failure is non-fatal."""
        # Prefer REDIS_URL env var (set by Railway/Heroku Redis plugins)
        redis_url = (
            settings.REDIS_URL
            or f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
        )

        # Skip connection attempt if pointing at localhost with no explicit URL configured
        # (avoids noisy errors when Redis simply isn't provisioned)
        if not settings.REDIS_URL and settings.REDIS_HOST == "localhost":
            logger.info("No Redis URL configured — running without caching")
            return

        self._connect_attempted = True
        try:
            self._redis_client = redis.from_url(
                redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                max_connections=20,
            )
            await self._redis_client.ping()
            self._connected = True
            logger.info(f"Connected to Redis at {redis_url}")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}")
            logger.info("Application will run without Redis caching")
            self._redis_client = None
            self._connected = False

    async def disconnect(self) -> None:
        """Close Redis connection"""
        if self._redis_client and self._connected:
            await self._redis_client.close()
            self._connected = False
            logger.info("Redis connection closed")

    @property
    def client(self) -> Optional[redis.Redis]:
        """Get Redis client instance"""
        if not self._connected or not self._redis_client:
            return None
        return self._redis_client

    @property
    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        return self._connected

    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis and deserialize JSON if applicable"""
        if not self.is_connected:
            return None

        try:
            value = await self.client.get(key)
            if value is None:
                return None

            # Try to deserialize JSON, fallback to string
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        except Exception as e:
            logger.error(f"Error getting key {key}: {e}")
            return None

    async def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Set value in Redis with optional expiration"""
        if not self.is_connected:
            return False

        try:
            # Serialize complex objects to JSON
            if isinstance(value, (dict, list)):
                serialized_value = json.dumps(value, default=str)
            else:
                serialized_value = value

            result = await self.client.set(key, serialized_value, ex=expire)
            return result
        except Exception as e:
            logger.error(f"Error setting key {key}: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete key from Redis"""
        if not self.is_connected:
            return False

        try:
            result = await self.client.delete(key)
            return result > 0
        except Exception as e:
            logger.error(f"Error deleting key {key}: {e}")
            return False

    async def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern"""
        if not self.is_connected:
            return 0

        try:
            keys = await self.client.keys(pattern)
            if keys:
                deleted = await self.client.delete(*keys)
                logger.info(f"Deleted {deleted} keys matching pattern: {pattern}")
                return deleted
            return 0
        except Exception as e:
            logger.error(f"Error deleting pattern {pattern}: {e}")
            return 0

    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis"""
        if not self.is_connected:
            return False

        try:
            return await self.client.exists(key) > 0
        except Exception as e:
            logger.error(f"Error checking existence of key {key}: {e}")
            return False

    async def expire(self, key: str, seconds: int) -> bool:
        """Set expiration time for a key"""
        if not self.is_connected:
            return False

        try:
            return await self.client.expire(key, seconds)
        except Exception as e:
            logger.error(f"Error setting expiration for key {key}: {e}")
            return False

    async def get_stats(self) -> Dict[str, Any]:
        """Get Redis stats"""
        if not self.is_connected:
            return {"connected": False}

        try:
            info = await self.client.info()
            return {
                "connected": True,
                "used_memory_human": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients"),
                "total_commands_processed": info.get("total_commands_processed"),
                "keyspace_hits": info.get("keyspace_hits"),
                "keyspace_misses": info.get("keyspace_misses"),
            }
        except Exception as e:
            logger.error(f"Error getting Redis stats: {e}")
            return {"connected": False, "error": str(e)}


# Global Redis client instance
redis_client = RedisClient()


async def get_redis_client() -> RedisClient:
    """Get Redis client instance (for dependency injection)"""
    if not redis_client._connect_attempted:
        await redis_client.connect()
    return redis_client
