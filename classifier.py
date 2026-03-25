"""Query classification and pattern matching."""

from models import QueryClassification


class QueryClassifier:
    """Classify incoming queries and route to appropriate modules."""

    # Keyword patterns mapped to modules
    CLASSIFICATION_PATTERNS = {
        "market_analysis": {
            "keywords": ["market", "industry", "trend", "growth", "segment", "TAM", "addressable", "demand", "adoption"],
            "confidence_threshold": 0.6,
        },
        "competitor_review": {
            "keywords": ["competitor", "competitive", "rival", "player", "benchmark", "vs", "comparison", "strategy", "positioning"],
            "confidence_threshold": 0.6,
        },
        "risk_assessment": {
            "keywords": ["risk", "threat", "mitigation", "exposure", "liability", "compliance", "regulation", "downside", "failure"],
            "confidence_threshold": 0.6,
        },
        "technical_audit": {
            "keywords": ["architecture", "technical", "design", "implementation", "system", "infrastructure", "code", "performance", "scalability"],
            "confidence_threshold": 0.6,
        },
    }

    def classify_query(self, query_text: str) -> QueryClassification:
        """
        Classify query and determine target module.

        Uses keyword matching with confidence scoring. Returns highest-confidence module,
        or defaults to 'market_analysis' if ambiguous.

        Args:
            query_text: The query string

        Returns:
            QueryClassification with module assignment and confidence
        """
        query_lower = query_text.lower()
        scores = {}

        # Score each module based on keyword matches
        for module, pattern_info in self.CLASSIFICATION_PATTERNS.items():
            keywords = pattern_info["keywords"]
            matches = sum(1 for kw in keywords if kw in query_lower)
            confidence = matches / len(keywords) if keywords else 0.0
            scores[module] = confidence

        # Find highest-scoring module
        best_module = max(scores, key=scores.get)
        best_confidence = scores[best_module]

        # Extract matched keywords
        matched_keywords = [
            kw for kw in self.CLASSIFICATION_PATTERNS[best_module]["keywords"]
            if kw in query_lower
        ]

        # Determine if we should use compact card or full framework
        # Ambiguous queries (low confidence) use full framework
        use_compact = best_confidence >= 0.4

        return QueryClassification(
            query_text=query_text,
            classified_module=best_module,
            confidence=best_confidence,
            keywords=matched_keywords,
            use_compact=use_compact,
        )

    def is_confident_classification(self, classification: QueryClassification) -> bool:
        """
        Check if classification meets confidence threshold.

        Args:
            classification: QueryClassification instance

        Returns:
            True if confidence meets threshold for the module
        """
        threshold = self.CLASSIFICATION_PATTERNS[classification.classified_module]["confidence_threshold"]
        return classification.confidence >= threshold

    @staticmethod
    def register_pattern(module_name: str, keywords: list[str], confidence_threshold: float = 0.6) -> None:
        """
        Register a new classification pattern (for extending system).

        Args:
            module_name: Name of module to route to
            keywords: List of keywords that trigger this module
            confidence_threshold: Minimum confidence required
        """
        QueryClassifier.CLASSIFICATION_PATTERNS[module_name] = {
            "keywords": keywords,
            "confidence_threshold": confidence_threshold,
        }
