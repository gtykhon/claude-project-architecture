"""Benchmark tool for token comparison and efficiency metrics."""

from module_loader import ModuleRegistry


def estimate_token_savings(compact_tokens: int, full_tokens: int) -> dict:
    """
    Calculate token savings metrics.

    Args:
        compact_tokens: Tokens used by compact card
        full_tokens: Tokens used by full framework

    Returns:
        Dictionary with savings metrics
    """
    savings = full_tokens - compact_tokens
    percentage = (savings / full_tokens * 100) if full_tokens > 0 else 0
    return {
        "tokens_saved": savings,
        "savings_percent": f"{percentage:.1f}%",
        "ratio": f"{compact_tokens}/{full_tokens}",
    }


def simulate_cache_hit_rate() -> dict:
    """
    Simulate cache hit rates based on typical usage patterns.

    Returns:
        Dictionary with simulated metrics
    """
    total_queries = 100
    unique_queries = 30
    repeated_queries = total_queries - unique_queries
    hit_rate = (repeated_queries / total_queries) * 100

    return {
        "total_queries": total_queries,
        "unique_queries": unique_queries,
        "repeated_queries": repeated_queries,
        "cache_hit_rate": f"{hit_rate:.1f}%",
        "description": f"{repeated_queries} of {total_queries} queries hit cache",
    }


def benchmark_all_modules() -> dict:
    """
    Benchmark all modules for token usage and efficiency.

    Returns:
        Dictionary with detailed benchmarking results
    """
    registry = ModuleRegistry()
    all_modules = registry.get_all_metadata()

    results = {
        "total_modules": len(all_modules),
        "modules": {},
        "summary": {
            "total_compact_tokens": 0,
            "total_full_tokens": 0,
            "total_tokens_saved": 0,
        }
    }

    for module_name, metadata in all_modules.items():
        savings = metadata.token_savings()
        savings_percent = metadata.savings_percentage()

        module_result = {
            "name": module_name,
            "description": metadata.description,
            "compact_tokens": metadata.compact_tokens,
            "full_tokens": metadata.full_tokens,
            "tokens_saved_per_hit": savings,
            "savings_percent": f"{savings_percent:.1f}%",
            "ttl_seconds": metadata.ttl_seconds,
        }

        results["modules"][module_name] = module_result
        results["summary"]["total_compact_tokens"] += metadata.compact_tokens
        results["summary"]["total_full_tokens"] += metadata.full_tokens
        results["summary"]["total_tokens_saved"] += savings

    # Calculate aggregate metrics
    total_full = results["summary"]["total_full_tokens"]
    total_compact = results["summary"]["total_compact_tokens"]
    total_saved = results["summary"]["total_tokens_saved"]

    results["summary"]["aggregate_savings_percent"] = (
        f"{(total_saved / total_full * 100):.1f}%" if total_full > 0 else "0%"
    )
    results["summary"]["average_tokens_per_module"] = (
        total_compact // len(all_modules) if all_modules else 0
    )

    return results


def benchmark_session_efficiency() -> dict:
    """
    Benchmark efficiency gains for a typical analysis session.

    Simulates a session with multiple analyses and cache hits.

    Returns:
        Dictionary with session-level metrics
    """
    # Typical session parameters
    analyses_per_session = 20
    hit_rate = 0.70  # 70% cache hit rate
    avg_full_tokens = 2000
    avg_compact_tokens = 850

    hits = int(analyses_per_session * hit_rate)
    misses = analyses_per_session - hits

    # Without caching (full framework always)
    tokens_without_cache = analyses_per_session * avg_full_tokens

    # With caching and compact cards
    tokens_with_cache = (hits * avg_compact_tokens) + (misses * avg_full_tokens)

    # Time estimation (tokens per millisecond ~= 1 token/ms for Claude)
    time_without_cache_ms = tokens_without_cache
    time_with_cache_ms = tokens_with_cache

    return {
        "analyses_per_session": analyses_per_session,
        "cache_hit_rate": f"{hit_rate * 100:.0f}%",
        "cache_hits": hits,
        "cache_misses": misses,
        "tokens": {
            "without_cache": tokens_without_cache,
            "with_cache": tokens_with_cache,
            "tokens_saved": tokens_without_cache - tokens_with_cache,
            "savings_percent": (
                f"{((tokens_without_cache - tokens_with_cache) / tokens_without_cache * 100):.0f}%"
            ),
        },
        "estimated_time": {
            "without_cache_ms": time_without_cache_ms,
            "with_cache_ms": time_with_cache_ms,
            "time_saved_ms": time_without_cache_ms - time_with_cache_ms,
            "time_savings_percent": (
                f"{((time_without_cache_ms - time_with_cache_ms) / time_without_cache_ms * 100):.0f}%"
            ),
        },
        "estimated_time_readable": {
            "without_cache": f"{time_without_cache_ms / 1000 / 60:.1f} minutes",
            "with_cache": f"{time_with_cache_ms / 1000 / 60:.1f} minutes",
        },
    }


def main():
    """Run all benchmarks and print results."""
    print("=" * 80)
    print("CLAUDE PROJECT ARCHITECTURE - BENCHMARKING REPORT")
    print("=" * 80)

    # Module-level benchmarking
    print("\n1. MODULE-LEVEL TOKEN USAGE")
    print("-" * 80)
    module_results = benchmark_all_modules()
    for module_name, module_data in module_results["modules"].items():
        print(f"\n{module_name.upper()}")
        print(f"  Compact:  {module_data['compact_tokens']:4d} tokens")
        print(f"  Full:     {module_data['full_tokens']:4d} tokens")
        print(f"  Savings:  {module_data['tokens_saved_per_hit']:4d} tokens ({module_data['savings_percent']})")

    print(f"\nAGGREGATE METRICS")
    print(f"  Total modules:            {module_results['total_modules']}")
    print(f"  Total compact tokens:     {module_results['summary']['total_compact_tokens']}")
    print(f"  Total full tokens:        {module_results['summary']['total_full_tokens']}")
    print(f"  Total tokens saved:       {module_results['summary']['total_tokens_saved']}")
    print(f"  Aggregate savings:        {module_results['summary']['aggregate_savings_percent']}")
    print(f"  Average per module:       {module_results['summary']['average_tokens_per_module']} tokens")

    # Session-level benchmarking
    print("\n2. SESSION-LEVEL EFFICIENCY")
    print("-" * 80)
    session_results = benchmark_session_efficiency()
    print(f"Analyses per session:      {session_results['analyses_per_session']}")
    print(f"Cache hit rate:            {session_results['cache_hit_rate']}")
    print(f"Cache hits:                {session_results['cache_hits']}")
    print(f"Cache misses:              {session_results['cache_misses']}")

    print(f"\nTOKEN USAGE")
    print(f"  Without cache:            {session_results['tokens']['without_cache']:,} tokens")
    print(f"  With cache:               {session_results['tokens']['with_cache']:,} tokens")
    print(f"  Tokens saved:             {session_results['tokens']['tokens_saved']:,} tokens")
    print(f"  Savings:                  {session_results['tokens']['savings_percent']}")

    print(f"\nTIME ESTIMATES")
    print(f"  Without cache:            {session_results['estimated_time_readable']['without_cache']}")
    print(f"  With cache:               {session_results['estimated_time_readable']['with_cache']}")
    print(f"  Time saved:               {session_results['estimated_time']['time_saved_ms']:.0f} ms")
    print(f"  Speedup:                  {session_results['estimated_time']['time_savings_percent']}")

    # Cache simulation
    print("\n3. CACHE HIT RATE SIMULATION")
    print("-" * 80)
    cache_results = simulate_cache_hit_rate()
    print(f"Total queries:             {cache_results['total_queries']}")
    print(f"Unique queries:            {cache_results['unique_queries']}")
    print(f"Repeated queries:          {cache_results['repeated_queries']}")
    print(f"Cache hit rate:            {cache_results['cache_hit_rate']}")
    print(f"Description:               {cache_results['description']}")

    print("\n" + "=" * 80)
    print("END OF BENCHMARKING REPORT")
    print("=" * 80)


if __name__ == "__main__":
    main()
