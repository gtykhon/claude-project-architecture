"""Competitive analysis module for competitor positioning and strategy assessment."""


def analyze(query: str, context: str = "") -> str:
    """
    Perform competitive analysis on the given query.

    Args:
        query: The competitive question
        context: Additional context

    Returns:
        Competitive analysis result
    """
    return f"""
COMPETITOR REVIEW FRAMEWORK

Question: {query}
Context: {context if context else 'Competitive analysis'}

FRAMEWORK COMPONENTS:

1. Competitor Identification
   - Direct competitors (same market, same value prop)
   - Indirect competitors (substitute solutions)
   - Emerging threats and new entrants
   - Potential acquirers

2. Competitive Positioning
   - Market positioning map (value vs cost, features vs simplicity)
   - Differentiation strategy analysis
   - Messaging and brand positioning
   - Go-to-market strategy

3. Product & Feature Comparison
   - Core product capabilities
   - Feature parity assessment
   - Roadmap analysis (if publicly available)
   - Technology stack comparison

4. Financial & Commercial Analysis
   - Pricing strategy and positioning
   - Revenue models and unit economics
   - Funding and capital efficiency
   - Market share estimates

5. Organizational & Execution
   - Team strength and key hires
   - Operational maturity
   - Customer satisfaction signals
   - Sales and marketing effectiveness

6. Strategic Vulnerabilities
   - Product gaps and weaknesses
   - Market coverage blind spots
   - Resource constraints
   - Dependency risks

7. Competitive Threats & Opportunities
   - Direct threats to your positioning
   - Partnership or acquisition opportunities
   - Market shift implications
"""


def get_compact_card() -> dict:
    """Get compact pattern card for competitor review."""
    return {
        "module": "competitor_review",
        "description": "Analyze competitors, positioning, and competitive strategy",
        "framework_type": "compact",
        "key_sections": [
            "Direct Competitors",
            "Positioning Map",
            "Feature Comparison",
            "Pricing & Unit Economics",
            "Strategic Vulnerabilities",
        ],
        "decision_points": [
            "Direct or indirect competition?",
            "Market leader or insurgent?",
            "Defensible moat or easily copied?",
        ],
        "output_format": "Competitive summary with 3-5 key insights",
        "typical_tokens": 750,
    }


def get_full_framework() -> dict:
    """Get full framework for competitor review."""
    return {
        "module": "competitor_review",
        "description": "Complete competitive analysis framework",
        "framework_type": "full",
        "sections": [
            "Competitor Identification",
            "Competitive Positioning",
            "Product & Feature Comparison",
            "Financial & Commercial Analysis",
            "Organizational & Execution",
            "Strategic Vulnerabilities",
            "Competitive Threats & Opportunities",
            "Defensive and Offensive Strategies",
        ],
        "typical_tokens": 1950,
    }
