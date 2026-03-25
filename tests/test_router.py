"""Tests for router and query classification functionality."""

import pytest
from fastapi.testclient import TestClient

from classifier import QueryClassifier
from models import QueryClassification
from router import app


class TestQueryClassifier:
    """Test suite for QueryClassifier class."""

    @pytest.fixture
    def classifier(self) -> QueryClassifier:
        """Create a fresh classifier instance for testing."""
        return QueryClassifier()

    def test_classify_market_query(self, classifier: QueryClassifier):
        """Test classification of market analysis query."""
        query = "What are the market trends in SaaS in 2026?"
        classification = classifier.classify_query(query)

        assert classification.classified_module == "market_analysis"
        assert classification.confidence > 0.4
        assert len(classification.keywords) > 0

    def test_classify_competitor_query(self, classifier: QueryClassifier):
        """Test classification of competitor review query."""
        query = "How does our product compare to competitors?"
        classification = classifier.classify_query(query)

        assert classification.classified_module == "competitor_review"
        assert len(classification.keywords) > 0

    def test_classify_risk_query(self, classifier: QueryClassifier):
        """Test classification of risk assessment query."""
        query = "What are the regulatory risks for our business?"
        classification = classifier.classify_query(query)

        assert classification.classified_module == "risk_assessment"
        assert len(classification.keywords) > 0

    def test_classify_technical_query(self, classifier: QueryClassifier):
        """Test classification of technical audit query."""
        query = "How scalable is our architecture?"
        classification = classifier.classify_query(query)

        assert classification.classified_module == "technical_audit"
        assert len(classification.keywords) > 0

    def test_ambiguous_query_uses_compact(self, classifier: QueryClassifier):
        """Test that ambiguous queries use compact framework."""
        query = "Tell me something"
        classification = classifier.classify_query(query)

        assert classification.use_compact is True

    def test_confident_query_uses_full_or_compact(self, classifier: QueryClassifier):
        """Test confident classification uses compact by default."""
        query = "What is the market growth rate?"
        classification = classifier.classify_query(query)

        assert classification.confidence >= 0.4

    def test_keyword_matching(self, classifier: QueryClassifier):
        """Test that keywords are correctly identified."""
        query = "Market trends and growth drivers"
        classification = classifier.classify_query(query)

        assert "market" in classification.keywords
        assert "growth" in classification.keywords
        assert "trend" in classification.keywords

    def test_is_confident_classification(self, classifier: QueryClassifier):
        """Test confidence threshold checking."""
        confident_query = "What is the market size in enterprise software?"
        confident_classification = classifier.classify_query(confident_query)
        assert classifier.is_confident_classification(confident_classification)

    def test_case_insensitive_classification(self, classifier: QueryClassifier):
        """Test that classification is case-insensitive."""
        query_lower = "what are the market trends"
        query_upper = "WHAT ARE THE MARKET TRENDS"

        classification_lower = classifier.classify_query(query_lower)
        classification_upper = classifier.classify_query(query_upper)

        assert classification_lower.classified_module == classification_upper.classified_module


class TestRouter:
    """Test suite for FastAPI router."""

    @pytest.fixture
    def client(self) -> TestClient:
        """Create a TestClient for the FastAPI app."""
        return TestClient(app)

    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "endpoints" in data
        assert "POST /analyze" in data["endpoints"]

    def test_analyze_endpoint_with_valid_query(self, client: TestClient):
        """Test analyze endpoint with valid query."""
        response = client.post("/analyze", json={
            "query": "What is the market opportunity in SaaS?",
            "context": "B2B markets",
        })

        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "What is the market opportunity in SaaS?"
        assert data["module"] == "market_analysis"
        assert data["is_cached"] is False
        assert data["execution_time_ms"] > 0

    def test_analyze_endpoint_empty_query(self, client: TestClient):
        """Test analyze endpoint with empty query."""
        response = client.post("/analyze", json={
            "query": "",
            "context": "",
        })

        assert response.status_code == 400

    def test_analyze_endpoint_cache_hit(self, client: TestClient):
        """Test analyze endpoint with cache hit."""
        query = {
            "query": "What is the market trend?",
            "context": "SaaS",
        }

        # First request (cache miss)
        response1 = client.post("/analyze", json=query)
        assert response1.json()["is_cached"] is False

        # Second request (cache hit)
        response2 = client.post("/analyze", json=query)
        assert response2.json()["is_cached"] is True

        # Second request should be faster
        assert response2.json()["execution_time_ms"] < response1.json()["execution_time_ms"]

    def test_cache_stats_endpoint(self, client: TestClient):
        """Test cache stats endpoint."""
        # Make some queries
        client.post("/analyze", json={"query": "Market trends?", "context": ""})
        client.post("/analyze", json={"query": "Market trends?", "context": ""})
        client.post("/analyze", json={"query": "Risk assessment?", "context": ""})

        response = client.get("/cache/stats")
        assert response.status_code == 200
        stats = response.json()

        assert stats["total_queries"] > 0
        assert stats["cache_hits"] >= 1
        assert 0 <= stats["hit_rate_percent"] <= 100

    def test_modules_endpoint(self, client: TestClient):
        """Test modules listing endpoint."""
        response = client.get("/modules")
        assert response.status_code == 200
        data = response.json()

        assert "modules" in data
        assert len(data["modules"]) > 0

        # Check that all modules have required fields
        for module in data["modules"]:
            assert "name" in module
            assert "description" in module
            assert "compact_tokens" in module
            assert "full_tokens" in module

    def test_classify_endpoint(self, client: TestClient):
        """Test query classification endpoint."""
        response = client.get("/classify", params={
            "query": "What is the market opportunity?"
        })

        assert response.status_code == 200
        data = response.json()

        assert data["module"] in ["market_analysis", "competitor_review", "risk_assessment", "technical_audit"]
        assert "confidence" in data
        assert "keywords" in data
        assert "use_compact" in data

    def test_clear_cache_endpoint(self, client: TestClient):
        """Test cache clearing endpoint."""
        # Add some data
        client.post("/analyze", json={"query": "Test query", "context": ""})

        # Clear cache
        response = client.post("/cache/clear")
        assert response.status_code == 200
        assert response.json()["status"] == "success"

        # Verify cache is empty
        stats = client.get("/cache/stats").json()
        assert stats["total_queries"] == 0

    def test_analyze_with_force_full_framework(self, client: TestClient):
        """Test analyze endpoint with force_full_framework flag."""
        query = {
            "query": "What is the market trend?",
            "context": "",
            "force_full_framework": True,
        }

        response = client.post("/analyze", json=query)
        assert response.status_code == 200
        data = response.json()

        # Should use more tokens when forcing full framework
        assert data["tokens_used"] > 800
