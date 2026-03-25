"""Caching layer for analysis results."""

import hashlib
import json
from datetime import datetime
from typing import Optional

from models import CachedResult, CacheStats


class AnalysisCache:
    """
    Content-hash based caching system with optional Redis backend.
    Falls back to in-memory dict if Redis unavailable.
    """

    def __init__(self, use_redis: bool = False, redis_host: str = "localhost", redis_port: int = 6379):
        """
        Initialize cache layer.

        Args:
            use_redis: Whether to use Redis backend
            redis_host: Redis server host
            redis_port: Redis server port
        """
        self.use_redis = use_redis
        self.redis_client = None
        self._in_memory_cache: dict[str, CachedResult] = {}
        self._stats = CacheStats()

        if use_redis:
            try:
                import redis
                self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
                self.redis_client.ping()
            except Exception as e:
                print(f"Redis unavailable ({e}), falling back to in-memory cache")
                self.use_redis = False

    @staticmethod
    def _hash_query(query_text: str, context: str = "") -> str:
        """
        Generate content hash for query + context.

        Args:
            query_text: The query string
            context: Optional context string

        Returns:
            SHA256 hash hex string
        """
        combined = f"{query_text}::{context}".lower().strip()
        return hashlib.sha256(combined.encode()).hexdigest()

    def get_cached_analysis(self, query_text: str, context: str = "") -> Optional[CachedResult]:
        """
        Retrieve cached analysis result.

        Args:
            query_text: The query string
            context: Optional context string

        Returns:
            CachedResult if found and not expired, None otherwise
        """
        query_hash = self._hash_query(query_text, context)

        if self.redis_client:
            cached_json = self.redis_client.get(query_hash)
            if cached_json:
                cached_data = json.loads(cached_json)
                result = CachedResult(**cached_data)
                if not result.is_expired():
                    self._stats.cache_hits += 1
                    result.mark_hit()
                    self.redis_client.setex(query_hash, result.ttl_seconds, cached_json)
                    return result
                else:
                    self.redis_client.delete(query_hash)

        else:
            if query_hash in self._in_memory_cache:
                result = self._in_memory_cache[query_hash]
                if not result.is_expired():
                    self._stats.cache_hits += 1
                    result.mark_hit()
                    return result
                else:
                    del self._in_memory_cache[query_hash]

        self._stats.cache_misses += 1
        return None

    def store_analysis(self, query_text: str, context: str, result: str, module: str, ttl_seconds: int = 86400) -> CachedResult:
        """
        Store analysis result in cache.

        Args:
            query_text: The query string
            context: Optional context string
            result: Analysis result text
            module: Name of module that produced result
            ttl_seconds: Time-to-live in seconds (default 24 hours)

        Returns:
            CachedResult instance
        """
        query_hash = self._hash_query(query_text, context)

        cached_result = CachedResult(
            query_hash=query_hash,
            result=result,
            module=module,
            ttl_seconds=ttl_seconds,
        )

        if self.redis_client:
            cached_json = json.dumps({
                "query_hash": cached_result.query_hash,
                "result": cached_result.result,
                "module": cached_result.module,
                "timestamp": cached_result.timestamp.isoformat(),
                "ttl_seconds": cached_result.ttl_seconds,
                "hit_count": cached_result.hit_count,
            })
            self.redis_client.setex(query_hash, ttl_seconds, cached_json)
        else:
            self._in_memory_cache[query_hash] = cached_result

        # Update stats
        self._stats.total_queries += 1
        if module not in self._stats.modules_cached:
            self._stats.modules_cached[module] = 0
        self._stats.modules_cached[module] += 1

        # Estimate cache size
        self._stats.cache_size_bytes += len(query_text) + len(context) + len(result)

        return cached_result

    def get_stats(self) -> CacheStats:
        """
        Get current cache statistics.

        Returns:
            CacheStats instance with hit rate, size, and module breakdown
        """
        self._stats.total_queries = self._stats.cache_hits + self._stats.cache_misses
        return self._stats

    def clear_cache(self) -> None:
        """Clear all cached results."""
        if self.redis_client:
            self.redis_client.flushdb()
        else:
            self._in_memory_cache.clear()
        self._stats = CacheStats()

    def get_all_cached_keys(self) -> list[str]:
        """
        Get all cached query hashes (for debugging/monitoring).

        Returns:
            List of query hash strings
        """
        if self.redis_client:
            return self.redis_client.keys("*")
        else:
            return list(self._in_memory_cache.keys())

    def cache_size(self) -> int:
        """Get number of items in cache."""
        if self.redis_client:
            return self.redis_client.dbsize()
        else:
            return len(self._in_memory_cache)
