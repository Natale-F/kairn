"""Integration tests for API endpoints"""

import json


class TestHealthEndpoints:
    """Test health check endpoints"""

    def test_root_endpoint(self, client, mock_env):
        """Test GET / returns service status"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "ok"
        assert "service" in data
        assert "version" in data
        assert data["mistral_api_configured"] is True

    def test_health_endpoint(self, client, mock_env):
        """Test GET /health returns detailed status"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"
        assert "api" in data
        assert data["api"]["mistral"] is True


class TestModelsEndpoint:
    """Test /api/tags endpoint"""

    def test_list_models(self, client, mock_env):
        """Test GET /api/tags returns available models"""
        response = client.get("/api/tags")

        assert response.status_code == 200
        data = response.json()

        assert "models" in data
        assert isinstance(data["models"], list)
        assert len(data["models"]) > 0

        # Check model structure
        model = data["models"][0]
        assert "name" in model
        assert "model" in model
        assert "details" in model

    def test_models_include_mistral_variants(self, client, mock_env):
        """Test that all Mistral variants are included"""
        response = client.get("/api/tags")
        data = response.json()

        model_names = [m["name"] for m in data["models"]]
        assert "mistral-large" in model_names
        assert "mistral-medium" in model_names
        assert "mistral-small" in model_names


class TestGenerateEndpoint:
    """Test /api/generate endpoint"""

    def test_generate_streaming(self, client, mock_env):
        """Test POST /api/generate with streaming"""
        request_data = {"model": "mistral-small", "prompt": "Tell me a story", "stream": True}

        response = client.post("/api/generate", json=request_data)

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/x-ndjson"

        # Parse NDJSON response
        lines = response.text.strip().split("\n")
        chunks = [json.loads(line) for line in lines if line]

        assert len(chunks) > 0

        # Last chunk should have done=True
        assert chunks[-1]["done"] is True

        # Other chunks should have content
        for chunk in chunks[:-1]:
            assert chunk["done"] is False
            assert "response" in chunk

    def test_generate_validation_error(self, client, mock_env):
        """Test generate with missing required fields"""
        request_data = {
            "model": "mistral-large"
            # Missing 'prompt' field
        }

        response = client.post("/api/generate", json=request_data)
        assert response.status_code == 422  # Validation error


class TestChatEndpoint:
    """Test /api/chat endpoint"""

    def test_chat_streaming(self, client, mock_env):
        """Test POST /api/chat with streaming"""
        request_data = {
            "model": "mistral-small",
            "messages": [{"role": "user", "content": "How are you?"}],
            "stream": True,
        }

        response = client.post("/api/chat", json=request_data)

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/x-ndjson"

        # Parse NDJSON response
        lines = response.text.strip().split("\n")
        chunks = [json.loads(line) for line in lines if line]

        assert len(chunks) > 0

        # Last chunk should have done=True
        assert chunks[-1]["done"] is True

        # Check message format
        for chunk in chunks:
            assert "message" in chunk
            assert chunk["message"]["role"] == "assistant"


class TestPullEndpoint:
    """Test /api/pull endpoint (mock)"""

    def test_pull_existing_model(self, client, mock_env):
        """Test pulling an existing model"""
        request_data = {"name": "mistral-large"}

        response = client.post("/api/pull", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "success"
        assert "digest" in data
        assert "total" in data
        assert "completed" in data

    def test_pull_nonexistent_model(self, client, mock_env):
        """Test pulling a model that doesn't exist"""
        request_data = {"name": "nonexistent-model"}

        response = client.post("/api/pull", json=request_data)

        assert response.status_code == 404
        data = response.json()
        assert "error" in data


class TestCORS:
    """Test CORS configuration"""

    def test_cors_headers(self, client, mock_env):
        """Test that CORS headers are set correctly"""
        response = client.options(
            "/api/tags",
            headers={"Origin": "http://localhost:3000", "Access-Control-Request-Method": "GET"},
        )

        # CORS should be configured
        assert "access-control-allow-origin" in response.headers or response.status_code == 200
