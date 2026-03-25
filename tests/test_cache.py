"""Tests for cache layer functionality."""

import pytest

from cache_layer import AnalysisCache
from models import CachedResult


class TestAnalysisCache:
    """Test suite for AnalysisCache class."""

    @pytest.fixture
    def cache(self) -> AnalysisCache:
        """Create a fresh cache instance for testing."""
        return AnalysisCache(use_redis=False)

    def test_cache_initialization(self, cache: AnalysisCache):
        """Test cache initializes correctly."""
        assert cache is not None
        assert cache.cache_size() == 0

    def test_store_and_retrieve_analysis(self, cache: AnalysisCache):
        """Test storing and retrieving an analysis."""
        query = "What is the market opportunity?"
        context = "SaaS markets"
        result = "Market analysis result"
        module = "market_analysis"

        cache.store_analysis(query, context, result, module)
        cached = cache.get_cached_analysis(query, context)

        assert cached is not None
        assert cached.result == result
        assert cached.module == module

    def test_cache_hit_rate(self, cache: AnalysisCache):
        """Test cache hit rate tracking."""
        query1 = "Market question"
        query2 = "Risk assessment"

        # Store two different analyses
        cache.store_analysis(query1, "", "result1", "market_analysis")
        cache.store_analysis(query2, "", "result2", "risk_assessment")

        # Retrieve first analysis (hit)
        cache.get_cached_analysis(query1, "")

        # Retrieve non-existent analysis (miss)
        cache.get_cached_analysis("unknown query", "")

        # Retrieve first again (hit)
        cache.get_cached_analysis(query1, "")

        stats = cache.get_stats()
        assert stats.cache_hits == 2
        assert stats.cache_misses == 1
        assert stats.hit_rate == pytest.approx(66.66, rel=0.1)

    def test_expiration(self, cache: AnalysisCache):
        """Test cache result expiration."""
        query = "Expiring query"
        cache.store_analysis(query, "", "result", "market_analysis", ttl_seconds=1)

        # Should exist immediately
        cached = cache.get_cached_analysis(query, "")
        assert cached is not None

        # Manually mark as expired
        cached.ttl_seconds = 0
        cached = cache.get_cached_analysis(query, "")
        assert cached is None

    def test_cache_context_matters(self, cache: AnalysisCache):
        """Test that context affects cache key."""
        query = "What is the market?"
        context1 = "SaaS"
        context2 = "Healthcare"

        cache.store_analysis(query, context1, "SaaS result", "market_analysis")
        cache.store_analysis(query, context2, "Healthcare result", "market_analysis")

        # Different contexts should have different cache entries
        saas_cached = cache.get_cached_analysis(query, context1)
        healthcare_cached = cache.get_cached_analysis(query, context2)

        assert saas_cached.result == "SaaS result"
        assert healthcare_cached.result == "Healthcare result"

    def test_cache_size_tracking(self, cache: AnalysisCache):
        """Test cache size tracking."""
        initial_size = cache._stats.cache_size_bytes

        cache.store_analysis("query1", "context1", "result1", "module1")
        cache.store_analysis("query2", "context2", "result2", "module2")

        final_size = cache._stats.cache_size_bytes
        assert final_size > initial_size

    def test_module_cache_tracking(self, cache: AnalysisCache):
        """Test tracking of cache entries by module."""
        cache.store_analysis("q1", "", "r1", "market_analysis")
        cache.store_analysis("q2", "", "r2", "market_analysis")
        cache.store_analysis("q3", "", "r3", "risk_assessment")

        stats = cache.get_stats()
        assert stats.modules_cached["market_analysis"] == 2
        assert stats.modules_cached["risk_assessment"] == 1

    def test_clear_cache(self, cache: AnalysisCache):
        """Test clearing cache."""
        cache.store_analysis("q1", "", "r1", "market_analysis")
        cache.store_analysis("q2", "", "r2", "risk_assessment")

        assert cache.cache_size() == 2

        cache.clear_cache()

        assert cache.cache_size() == 0
        stats = cache.get_stats()
        assert stats.cache_hits == 0
        assert stats.cache_misses == 0

    def test_hash_consistency(self, cache: AnalysisCache):
        """Test that query hashing is consistent."""
        query = "What is the market?"
        context = "B2B"

        hash1 = cache._hash_query(query, context)
        hash2 = cache._hash_query(query, context)

        assert hash1 == hash2

    def test_hash_case_insensitive(self, cache: AnalysisCache):
        """Test that hashing is case-insensitive."""
        hash1 = cache._hash_query("What is the market?", "B2B")
        hash2 = cache._hash_query("WHAT IS THE MARKET?", "b2b")

        assert hash1 == hash2

    def test_hit_count_increments(self, cache: AnalysisCache):
        """Test that hit count increments on cache hits."""
        query = "Test query"
        cache.store_analysis(query, "", "result", "market_analysis")

        cached = cache.get_cached_analysis(query, "")
        assert cached.hit_count == 1

        cached = cache.get_cached_analysis(query, "")
        assert cached.hit_count == 2
