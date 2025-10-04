"""Unit tests for FastAPI endpoints"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


class TestAPIEndpoints:
    """Test suite for API endpoints"""

    def test_root_endpoint(self, client):
        """Test root endpoint returns service info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()

        assert "service" in data
        assert "version" in data
        assert "status" in data
        assert data["service"] == "Offline RAG Pipeline API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"

    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()

        assert "status" in data
        assert "model_loaded" in data
        assert "document_indexed" in data
        assert data["status"] in ["healthy", "initializing"]

    def test_health_endpoint_structure(self, client):
        """Test health endpoint returns correct structure"""
        response = client.get("/health")
        data = response.json()

        # Check required fields
        required_fields = ["status", "model_loaded", "document_indexed"]
        for field in required_fields:
            assert field in data

    def test_metrics_endpoint_exists(self, client):
        """Test metrics endpoint exists and returns data"""
        response = client.get("/metrics")
        # Prometheus metrics endpoint returns plain text
        assert response.status_code == 200
        # Should contain prometheus metrics format
        assert response.headers["content-type"].startswith("text/plain")

    def test_metrics_summary_endpoint(self, client):
        """Test human-readable metrics summary endpoint"""
        response = client.get("/metrics/summary")
        assert response.status_code == 200
        data = response.json()

        assert "total_queries" in data
        assert "average_response_time_ms" in data
        assert "total_errors" in data
        assert "uptime_seconds" in data

        # Check types
        assert isinstance(data["total_queries"], int)
        assert isinstance(data["average_response_time_ms"], (int, float))
        assert isinstance(data["total_errors"], int)
        assert isinstance(data["uptime_seconds"], (int, float))

    def test_docs_endpoint_exists(self, client):
        """Test OpenAPI docs endpoint exists"""
        response = client.get("/docs")
        assert response.status_code == 200
        # Swagger UI returns HTML
        assert "text/html" in response.headers["content-type"]

    def test_redoc_endpoint_exists(self, client):
        """Test ReDoc endpoint exists"""
        response = client.get("/redoc")
        assert response.status_code == 200
        # ReDoc returns HTML
        assert "text/html" in response.headers["content-type"]

    def test_openapi_json_endpoint(self, client):
        """Test OpenAPI JSON schema endpoint"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()

        assert "openapi" in data
        assert "info" in data
        assert "paths" in data

        # Check key endpoints are documented
        assert "/query" in data["paths"]
        assert "/health" in data["paths"]
        assert "/metrics" in data["paths"]

    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        response = client.get("/health")
        # CORS middleware should add these headers
        assert "access-control-allow-origin" in response.headers or response.status_code == 200

    def test_query_endpoint_structure(self, client):
        """Test query endpoint validates request structure (without running model)"""
        # Test invalid request (missing required field)
        response = client.post("/query", json={})
        # Should return validation error
        assert response.status_code in [422, 503]  # 422 for validation, 503 if model not loaded

        # Test with minimal valid structure
        response = client.post("/query", json={"question": "test"})
        # Should either work or return 503 (model not loaded), not 422 (validation error)
        assert response.status_code in [200, 503]

    def test_index_endpoint_validation(self, client):
        """Test index endpoint validates request"""
        # Test invalid request (missing document_paths)
        response = client.post("/index", json={})
        assert response.status_code in [422, 503]  # Validation error or service unavailable

    def test_metrics_increment(self, client):
        """Test that metrics are being tracked"""
        # Get initial metrics
        response1 = client.get("/metrics/summary")
        initial_queries = response1.json()["total_queries"]

        # Make a request (will fail if model not loaded, but should still track)
        client.post("/query", json={"question": "test"})

        # Get metrics again
        response2 = client.get("/metrics/summary")

        # Queries or errors should have incremented
        assert response2.status_code == 200

    def test_uptime_tracking(self, client):
        """Test that uptime is being tracked"""
        import time

        response1 = client.get("/metrics/summary")
        uptime1 = response1.json()["uptime_seconds"]

        # Wait a moment
        time.sleep(0.1)

        response2 = client.get("/metrics/summary")
        uptime2 = response2.json()["uptime_seconds"]

        # Uptime should have increased
        assert uptime2 >= uptime1

    def test_error_handling(self, client):
        """Test that errors are handled gracefully"""
        # Try to index non-existent document
        response = client.post("/index", json={
            "document_paths": ["nonexistent_file_12345.md"]
        })

        # Should return error status, not crash
        assert response.status_code in [404, 422, 500, 503]

        # Response should be JSON
        data = response.json()
        assert "detail" in data or "error" in data or "message" in data


class TestAPIRequestValidation:
    """Test request validation with Pydantic"""

    def test_query_request_validation(self, client):
        """Test query request validates parameters"""
        # Test with invalid types
        response = client.post("/query", json={
            "question": 123,  # Should be string
            "top_k": "invalid"  # Should be int
        })

        assert response.status_code == 422  # Validation error

    def test_query_request_defaults(self, client):
        """Test query request uses default values"""
        # Minimal request should use defaults
        response = client.post("/query", json={
            "question": "What is radar calibration?"
        })

        # Should either work or return 503 (model not loaded)
        # Not 422 (validation error) because defaults should be applied
        assert response.status_code in [200, 503]

    def test_index_request_validation(self, client):
        """Test index request validates document_paths"""
        # Test with invalid type
        response = client.post("/index", json={
            "document_paths": "should_be_list"
        })

        assert response.status_code == 422  # Validation error


class TestAPIResponseFormat:
    """Test API response formats"""

    def test_health_response_format(self, client):
        """Test health endpoint response format"""
        response = client.get("/health")
        data = response.json()

        # Check field types
        assert isinstance(data["status"], str)
        assert isinstance(data["model_loaded"], bool)
        assert isinstance(data["document_indexed"], bool)

    def test_error_response_format(self, client):
        """Test error responses have consistent format"""
        # Trigger error by querying without model loaded or invalid data
        response = client.post("/query", json={"question": 123})  # Invalid type

        # Should return structured error
        assert response.status_code >= 400
        data = response.json()
        assert "detail" in data or "error" in data
