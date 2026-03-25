"""Market analysis module for analyzing market trends and opportunities."""


def analyze(query: str, context: str = "") -> str:
    """
    Perform market analysis on the given query.

    Args:
        query: The market question
        context: Additional context

    Returns:
        Market analysis result
    """
    return f"""
MARKET ANALYSIS FRAMEWORK

Question: {query}
Context: {context if context else 'General market analysis'}

FRAMEWORK COMPONENTS:

1. Market Definition & Sizing
   - Total Addressable Market (TAM) calculation
   - Serviceable Addressable Market (SAM) identification
   - Serviceable Obtainable Market (SOM) projection

2. Market Trends & Drivers
   - Growth drivers (macro, industry, regulatory)
   - Market headwinds and constraints
   - Adoption curves and inflection points

3. Segmentation Analysis
   - Key market segments and niches
   - Segment attractiveness matrix
   - Geographic and vertical variations

4. Competitive Landscape
   - Direct and indirect competitors
   - Competitive positioning map
   - Market consolidation trends

5. Risk Factors
   - Market risk assessment
   - Regulatory and compliance risks
   - Technology obsolescence risks

6. Opportunity Sizing
   - Near-term opportunities (0-2 years)
   - Medium-term opportunities (2-5 years)
   - Long-term opportunities (5+ years)
"""


def get_compact_card() -> dict:
    """Get compact pattern card for market analysis."""
    return {
        "module": "market_analysis",
        "description": "Analyze market trends, growth drivers, and opportunity sizing",
        "framework_type": "compact",
        "key_sections": [
            "Market Definition & Sizing (TAM/SAM/SOM)",
            "Growth Drivers",
            "Segmentation",
            "Competitive Position",
            "Risk Assessment",
        ],
        "decision_points": [
            "Is TAM > $10B?",
            "Growth rate > 20% CAGR?",
            "Market consolidating or fragmenting?",
        ],
        "output_format": "Executive summary with 3-5 key insights",
        "typical_tokens": 800,
    }


def get_full_framework() -> dict:
    """Get full framework for market analysis."""
    return {
        "module": "market_analysis",
        "description": "Complete market analysis framework",
        "framework_type": "full",
        "sections": [
            "Market Definition & Sizing",
            "Market Trends & Drivers",
            "Segmentation Analysis",
            "Competitive Landscape",
            "Risk Factors",
            "Opportunity Sizing",
            "Financial Projections",
            "Go-to-Market Implications",
        ],
        "typical_tokens": 2100,
    }
