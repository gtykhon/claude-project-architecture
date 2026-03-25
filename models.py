"""Data models for Claude Project Architecture."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class CachedResult:
    """Result stored in cache layer."""

    query_hash: str
    result: str
    module: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    ttl_seconds: int = 86400  # 24 hours default
    hit_count: int = 0

    def is_expired(self) -> bool:
        """Check if cached result has expired."""
        elapsed = (datetime.utcnow() - self.timestamp).total_seconds()
        return elapsed > self.ttl_seconds

    def mark_hit(self) -> None:
        """Increment hit counter."""
        self.hit_count += 1


@dataclass
class QueryClassification:
    """Result of query classification."""

    query_text: str
    classified_module: str
    confidence: float
    keywords: list[str] = field(default_factory=list)
    use_compact: bool = True  # Use compact card if True, full framework if False


@dataclass
class AnalyticalModule:
    """Metadata and interface for an analytical module."""

    name: str
    description: str
    keywords: list[str]
    compact_tokens: int  # Estimated tokens for compact card
    full_tokens: int     # Estimated tokens for full framework
    ttl_seconds: int = 604800  # 7 days default

    def token_savings(self) -> int:
        """Calculate token savings using compact card."""
        return self.full_tokens - self.compact_tokens

    def savings_percentage(self) -> float:
        """Calculate percentage savings."""
        if self.full_tokens == 0:
            return 0.0
        return (self.token_savings() / self.full_tokens) * 100


@dataclass
class RoutingDecision:
    """Decision to route query to specific module."""

    query_classification: QueryClassification
    selected_module: str
    cache_hit: bool
    cached_result: Optional[CachedResult] = None
    use_compact: bool = True


@dataclass
class AnalysisResult:
    """Complete analysis result."""

    query: str
    module: str
    result: str
    is_cached: bool
    timestamp: datetime = field(default_factory=datetime.utcnow)
    execution_time_ms: float = 0.0
    tokens_used: int = 0
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CacheStats:
    """Cache statistics and metrics."""

    total_queries: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    cache_size_bytes: int = 0
    modules_cached: dict[str, int] = field(default_factory=dict)  # module -> count

    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate."""
        if self.total_queries == 0:
            return 0.0
        return (self.cache_hits / self.total_queries) * 100

    @property
    def miss_rate(self) -> float:
        """Calculate cache miss rate."""
        return 100 - self.hit_rate
