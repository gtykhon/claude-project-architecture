"""Risk assessment module for identifying and mitigating risks."""


def analyze(query: str, context: str = "") -> str:
    """
    Perform risk assessment on the given query.

    Args:
        query: The risk question
        context: Additional context

    Returns:
        Risk assessment result
    """
    return f"""
RISK ASSESSMENT FRAMEWORK

Question: {query}
Context: {context if context else 'Risk assessment'}

FRAMEWORK COMPONENTS:

1. Risk Identification
   - Operational risks (process, execution, dependencies)
   - Market risks (demand, competition, adoption)
   - Financial risks (unit economics, burn rate, funding)
   - Technology risks (technical debt, scalability, obsolescence)
   - Regulatory and compliance risks
   - People and organizational risks

2. Risk Quantification
   - Probability assessment (low/medium/high)
   - Impact assessment (small/medium/critical)
   - Risk scoring (probability × impact)
   - Risk ranking by severity

3. Risk Dependencies
   - Risks that trigger other risks (cascading effects)
   - Correlated risks (economic downturn triggers multiple risks)
   - Timing and sequencing of risks

4. Exposure Analysis
   - Current state exposure (unmitigated)
   - Financial downside from each risk
   - Confidence intervals and scenarios

5. Mitigation Strategies
   - Risk avoidance (eliminate the risk)
   - Risk reduction (minimize probability or impact)
   - Risk transfer (insurance, partnerships)
   - Risk acceptance (monitor and respond)

6. Monitoring & Response Plans
   - Early warning indicators
   - Trigger thresholds for escalation
   - Response playbooks and contingency plans
   - Ownership and accountability

7. Scenario Analysis
   - Best case scenario (risks don't materialize)
   - Base case scenario (expected outcomes)
   - Worst case scenario (critical risks materialize)
   - Alternative futures

8. Strategic Implications
   - Impact on competitive position
   - Strategic pivot triggers
   - Investment and resource implications
"""


def get_compact_card() -> dict:
    """Get compact pattern card for risk assessment."""
    return {
        "module": "risk_assessment",
        "description": "Identify, quantify, and mitigate risks",
        "framework_type": "compact",
        "key_sections": [
            "Risk Identification",
            "Probability & Impact",
            "Risk Ranking",
            "Mitigation Strategies",
            "Monitoring Plan",
        ],
        "decision_points": [
            "Critical, High, Medium, or Low severity?",
            "Can we mitigate this risk?",
            "Is this a showstopper?",
        ],
        "output_format": "Risk summary with ranked top 5 risks and mitigation",
        "typical_tokens": 900,
    }


def get_full_framework() -> dict:
    """Get full framework for risk assessment."""
    return {
        "module": "risk_assessment",
        "description": "Complete risk assessment framework",
        "framework_type": "full",
        "sections": [
            "Risk Identification",
            "Risk Quantification",
            "Risk Dependencies",
            "Exposure Analysis",
            "Mitigation Strategies",
            "Monitoring & Response Plans",
            "Scenario Analysis",
            "Strategic Implications",
            "Risk Governance",
        ],
        "typical_tokens": 2300,
    }
