import json
import logging
from typing import Any, Optional, Dict, List, Callable
from functools import wraps
import hashlib
from app.core.redis_client import redis_client
from app.core.config import settings

logger = logging.getLogger(__name__)


class CacheService:
    """Service for handling application-level caching with Redis"""
    
    def __init__(self):
        self.default_ttl = settings.CACHE_TTL_DEFAULT
        self.prefix = "arkham:"
    
    def _generate_cache_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate a consistent cache key from function arguments"""
        # Create a string representation of all arguments
        key_data = f"{prefix}:{args}:{sorted(kwargs.items())}"
        # Hash long keys to avoid Redis key length limits
        if len(key_data) > 200:
            key_hash = hashlib.md5(key_data.encode()).hexdigest()
            return f"{self.prefix}{prefix}:hash:{key_hash}"
        return f"{self.prefix}{prefix}:{key_data}"
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            return await redis_client.get(key)
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with optional TTL"""
        try:
            ttl = ttl or self.default_ttl
            return await redis_client.set(key, value, expire=ttl)
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            return await redis_client.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    async def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern"""
        try:
            full_pattern = f"{self.prefix}{pattern}"
            return await redis_client.delete_pattern(full_pattern)
        except Exception as e:
            logger.error(f"Cache delete pattern error: {e}")
            return 0
    
    async def get_with_key(self, cache_type: str, identifier: str, **kwargs) -> Optional[Any]:
        """Get cached data with flexible key generation"""
        key = self._build_cache_key(cache_type, identifier, **kwargs)
        return await self.get(key)
    
    async def set_with_key(self, cache_type: str, identifier: str, data: Any, ttl: Optional[int] = None, **kwargs) -> bool:
        """Set cached data with flexible key generation"""
        key = self._build_cache_key(cache_type, identifier, **kwargs)
        return await self.set(key, data, ttl=ttl)
    
    async def delete_with_key(self, cache_type: str, identifier: str, **kwargs) -> bool:
        """Delete cached data with flexible key generation"""
        key = self._build_cache_key(cache_type, identifier, **kwargs)
        return await self.delete(key)
    
    def _build_cache_key(self, cache_type: str, identifier: str, **kwargs) -> str:
        """Build cache key dynamically"""
        key_parts = [self.prefix, cache_type, str(identifier)]
        
        # Add any additional parameters to the key
        if kwargs:
            sorted_kwargs = sorted(kwargs.items())
            for k, v in sorted_kwargs:
                if isinstance(v, (list, tuple)):
                    # Convert lists/tuples to sorted string
                    v = ":".join(sorted(map(str, v)))
                key_parts.append(f"{k}:{v}")
        
        return ":".join(key_parts)
    
    async def invalidate_by_pattern(self, cache_type: str, pattern: str = "*") -> int:
        """Invalidate cache entries by pattern"""
        full_pattern = f"{self.prefix}{cache_type}:{pattern}"
        deleted = await self.delete_pattern(full_pattern)
        logger.info(f"Cleared {deleted} cache entries for pattern: {full_pattern}")
        return deleted
    
    async def invalidate_by_tags(self, *tags: str) -> int:
        """Invalidate multiple cache patterns by tags"""
        total_deleted = 0
        for tag in tags:
            deleted = await self.invalidate_by_pattern(tag, "*")
            total_deleted += deleted
        return total_deleted


def cache_result(prefix: str, ttl: Optional[int] = None):
    """Decorator to cache function results"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_service = CacheService()
            
            # Generate cache key
            cache_key = cache_service._generate_cache_key(prefix, *args, **kwargs)
            
            # Try to get from cache first
            cached_result = await cache_service.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for key: {cache_key}")
                return cached_result
            
            # Execute function and cache result
            logger.debug(f"Cache miss for key: {cache_key}")
            result = await func(*args, **kwargs)
            
            # Cache the result
            await cache_service.set(cache_key, result, ttl)
            return result
        
        return wrapper
    return decorator


# Global cache service instance
cache_service = CacheService()