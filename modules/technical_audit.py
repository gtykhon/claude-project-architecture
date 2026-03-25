"""Technical audit module for architecture and implementation review."""


def analyze(query: str, context: str = "") -> str:
    """
    Perform technical audit on the given query.

    Args:
        query: The technical question
        context: Additional context

    Returns:
        Technical audit result
    """
    return f"""
TECHNICAL AUDIT FRAMEWORK

Question: {query}
Context: {context if context else 'Technical audit'}

FRAMEWORK COMPONENTS:

1. Architecture Review
   - System design and decomposition
   - Component interactions and dependencies
   - Scalability and performance characteristics
   - Technology choices and tradeoffs

2. Code Quality Assessment
   - Code organization and modularity
   - Design patterns and best practices
   - Test coverage and testing strategies
   - Documentation and maintainability

3. Performance & Optimization
   - Bottleneck identification (CPU, memory, I/O)
   - Query and operation performance
   - Caching strategies
   - Resource utilization optimization

4. Scalability Analysis
   - Current capacity and limits
   - Horizontal and vertical scaling paths
   - Database and storage scaling
   - Stateless vs stateful components

5. Reliability & Resilience
   - Failure modes and dependencies
   - Redundancy and failover mechanisms
   - Circuit breakers and degradation paths
   - Disaster recovery and business continuity

6. Security Assessment
   - Authentication and authorization
   - Data encryption (transit and at rest)
   - Vulnerability scanning and penetration testing
   - Security best practices and compliance

7. Operations & Observability
   - Monitoring and alerting
   - Logging and debugging capabilities
   - Operational runbooks
   - Release and deployment processes

8. Technical Debt
   - Known issues and workarounds
   - Legacy code and outdated dependencies
   - Refactoring opportunities
   - Modernization priorities

9. Infrastructure
   - Hosting and cloud architecture
   - Container and orchestration strategy
   - Configuration management
   - Infrastructure as code practices
"""


def get_compact_card() -> dict:
    """Get compact pattern card for technical audit."""
    return {
        "module": "technical_audit",
        "description": "Review technical architecture and implementation",
        "framework_type": "compact",
        "key_sections": [
            "Architecture Overview",
            "Scalability Assessment",
            "Performance Issues",
            "Security Posture",
            "Technical Debt",
        ],
        "decision_points": [
            "Monolith or microservices?",
            "Stateless or stateful?",
            "Database bottleneck?",
        ],
        "output_format": "Technical summary with top issues and recommendations",
        "typical_tokens": 850,
    }


def get_full_framework() -> dict:
    """Get full framework for technical audit."""
    return {
        "module": "technical_audit",
        "description": "Complete technical audit framework",
        "framework_type": "full",
        "sections": [
            "Architecture Review",
            "Code Quality Assessment",
            "Performance & Optimization",
            "Scalability Analysis",
            "Reliability & Resilience",
            "Security Assessment",
            "Operations & Observability",
            "Technical Debt",
            "Infrastructure",
            "Modernization Strategy",
        ],
        "typical_tokens": 2200,
    }
