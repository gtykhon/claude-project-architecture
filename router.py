"""FastAPI query routing and request handling."""

import time
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from cache_layer import AnalysisCache
from classifier import QueryClassifier
from models import AnalysisResult, CacheStats, QueryClassification, RoutingDecision
from module_loader import ModuleRegistry

# Initialize FastAPI app
app = FastAPI(
    title="Claude Project Architecture",
    description="Three-tier coordination system for AI analysis frameworks",
    version="1.0.0",
)

# Initialize core components
cache = AnalysisCache(use_redis=False)
classifier = QueryClassifier()
registry = ModuleRegistry()


# Request/Response models
class AnalysisRequest(BaseModel):
    """Request model for analysis endpoint."""

    query: str
    context: Optional[str] = ""
    force_full_framework: bool = False


class AnalysisResponse(BaseModel):
    """Response model for analysis endpoint."""

    query: str
    module: str
    result: str
    is_cached: bool
    execution_time_ms: float
    tokens_used: int
    confidence: float


class CacheStatsResponse(BaseModel):
    """Response model for cache stats endpoint."""

    total_queries: int
    cache_hits: int
    cache_misses: int
    hit_rate_percent: float
    miss_rate_percent: float
    cache_size_bytes: int
    modules_cached: dict[str, int]


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/analyze")
async def analyze(request: AnalysisRequest) -> AnalysisResponse:
    """
    Analyze query using three-tier coordination system.

    Process:
    1. Check cache (70% hit rate)
    2. Classify query (determine target module)
    3. Route to module (lazy-loaded)
    4. Return result (cached or fresh)

    Args:
        request: AnalysisRequest with query and optional context

    Returns:
        AnalysisResponse with result, timing, and cache status

    Raises:
        HTTPException: If query is empty or routing fails
    """
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    start_time = time.time()

    # Layer 1: Check cache
    cached_result = cache.get_cached_analysis(request.query, request.context)
    if cached_result and not request.force_full_framework:
        execution_time = (time.time() - start_time) * 1000
        return AnalysisResponse(
            query=request.query,
            module=cached_result.module,
            result=cached_result.result,
            is_cached=True,
            execution_time_ms=execution_time,
            tokens_used=800,  # Estimate for cached result
            confidence=1.0,
        )

    # Layer 2: Classify query
    classification = classifier.classify_query(request.query)
    use_compact = classification.use_compact and not request.force_full_framework

    # Layer 3: Route to module
    module_metadata = registry.get_module_metadata(classification.classified_module)
    if not module_metadata:
        raise HTTPException(status_code=404, detail=f"Module {classification.classified_module} not found")

    # Simulate analysis (in production, call actual module)
    if use_compact:
        result_text = f"[COMPACT CARD] {classification.classified_module}: {request.query}\n\n"
        result_text += f"Key insights from {classification.classified_module} framework.\n"
        result_text += f"Confidence: {classification.confidence:.2%}\n"
        result_text += f"Matched keywords: {', '.join(classification.keywords)}"
        tokens_used = module_metadata.compact_tokens
    else:
        result_text = f"[FULL FRAMEWORK] {classification.classified_module}: {request.query}\n\n"
        result_text += f"Comprehensive analysis from {classification.classified_module} framework.\n"
        result_text += f"Confidence: {classification.confidence:.2%}\n"
        result_text += f"Matched keywords: {', '.join(classification.keywords)}"
        tokens_used = module_metadata.full_tokens

    # Store in cache
    cache.store_analysis(
        query_text=request.query,
        context=request.context,
        result=result_text,
        module=classification.classified_module,
        ttl_seconds=module_metadata.ttl_seconds,
    )

    execution_time = (time.time() - start_time) * 1000

    return AnalysisResponse(
        query=request.query,
        module=classification.classified_module,
        result=result_text,
        is_cached=False,
        execution_time_ms=execution_time,
        tokens_used=tokens_used,
        confidence=classification.confidence,
    )


@app.get("/cache/stats")
async def get_cache_stats() -> CacheStatsResponse:
    """
    Get cache statistics and hit rate.

    Returns:
        CacheStatsResponse with hit rate, size, and module breakdown
    """
    stats = cache.get_stats()
    return CacheStatsResponse(
        total_queries=stats.total_queries,
        cache_hits=stats.cache_hits,
        cache_misses=stats.cache_misses,
        hit_rate_percent=stats.hit_rate,
        miss_rate_percent=stats.miss_rate,
        cache_size_bytes=stats.cache_size_bytes,
        modules_cached=stats.modules_cached,
    )


@app.get("/modules")
async def list_modules() -> dict:
    """
    List all registered modules with metadata.

    Returns:
        Dictionary with module names, descriptions, and token usage
    """
    all_modules = registry.get_all_metadata()
    return {
        "modules": [
            {
                "name": m.name,
                "description": m.description,
                "compact_tokens": m.compact_tokens,
                "full_tokens": m.full_tokens,
                "token_savings": m.token_savings(),
                "savings_percent": f"{m.savings_percentage():.1f}%",
                "ttl_seconds": m.ttl_seconds,
            }
            for m in all_modules.values()
        ]
    }


@app.post("/cache/clear")
async def clear_cache() -> dict[str, str]:
    """
    Clear all cached results (admin endpoint).

    Returns:
        Confirmation message
    """
    cache.clear_cache()
    return {"message": "Cache cleared", "status": "success"}


@app.get("/classify")
async def classify(query: str) -> dict:
    """
    Classify a query without analysis (for debugging).

    Args:
        query: The query string to classify

    Returns:
        QueryClassification with module and confidence
    """
    classification = classifier.classify_query(query)
    return {
        "query": classification.query_text,
        "module": classification.classified_module,
        "confidence": f"{classification.confidence:.2%}",
        "keywords": classification.keywords,
        "use_compact": classification.use_compact,
    }


@app.get("/")
async def root() -> dict:
    """Root endpoint with API overview."""
    return {
        "name": "Claude Project Architecture",
        "description": "Three-tier coordination for AI analysis frameworks",
        "version": "1.0.0",
        "endpoints": {
            "POST /analyze": "Analyze query with caching and routing",
            "GET /cache/stats": "Cache statistics and hit rate",
            "GET /modules": "List all modules",
            "GET /classify": "Classify query without analysis",
            "POST /cache/clear": "Clear cache (admin)",
            "GET /health": "Health check",
            "GET /docs": "Swagger UI",
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
