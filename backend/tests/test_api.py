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
    """Test /v1/models endpoint (OpenAI format)"""

    def test_list_models(self, client, mock_env):
        """Test GET /v1/models returns available models"""
        response = client.get("/v1/models")

        assert response.status_code == 200
        data = response.json()

        assert "data" in data
        assert data["object"] == "list"
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0

        # Check model structure (OpenAI format)
        model = data["data"][0]
        assert "id" in model
        assert "object" in model
        assert model["object"] == "model"
        assert "created" in model
        assert "owned_by" in model

    def test_models_alternative_endpoint(self, client, mock_env):
        """Test GET /models also works (without /v1 prefix)"""
        response = client.get("/models")

        assert response.status_code == 200
        data = response.json()

        assert "data" in data
        assert data["object"] == "list"

    def test_models_include_mistral_variants(self, client, mock_env):
        """Test that all Mistral variants are included"""
        response = client.get("/v1/models")
        data = response.json()

        model_ids = [m["id"] for m in data["data"]]
        assert "mistral-large" in model_ids
        assert "mistral-medium" in model_ids


class TestChatCompletionsEndpoint:
    """Test /v1/chat/completions endpoint (OpenAI format)"""

    def test_chat_streaming(self, client, mock_env):
        """Test POST /v1/chat/completions with streaming"""
        request_data = {
            "model": "mistral-large",
            "messages": [{"role": "user", "content": "How are you?"}],
            "stream": True,
        }

        response = client.post("/v1/chat/completions", json=request_data)

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

        # Parse SSE response
        lines = response.text.strip().split("\n")
        data_lines = [line for line in lines if line.startswith("data: ")]

        assert len(data_lines) > 0

        # Check for [DONE] marker
        assert data_lines[-1] == "data: [DONE]"

        # Parse JSON chunks (excluding [DONE])
        chunks = []
        for line in data_lines[:-1]:
            chunk_data = line[6:]  # Remove "data: " prefix
            if chunk_data and not chunk_data.startswith("[DONE]"):
                chunks.append(json.loads(chunk_data))

        assert len(chunks) > 0

        # Check chunk format (OpenAI format)
        for chunk in chunks:
            assert "id" in chunk
            assert "object" in chunk
            assert chunk["object"] == "chat.completion.chunk"
            assert "model" in chunk
            assert "choices" in chunk
            assert len(chunk["choices"]) > 0
            assert "index" in chunk["choices"][0]
            assert "delta" in chunk["choices"][0]

    def test_chat_non_streaming(self, client, mock_env):
        """Test POST /v1/chat/completions without streaming"""
        request_data = {
            "model": "mistral-large",
            "messages": [{"role": "user", "content": "Say hello"}],
            "stream": False,
        }

        response = client.post("/v1/chat/completions", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Check response format (OpenAI format)
        assert "id" in data
        assert "object" in data
        assert data["object"] == "chat.completion"
        assert "model" in data
        assert data["model"] == "mistral-large"
        assert "choices" in data
        assert len(data["choices"]) > 0

        # Check choice structure
        choice = data["choices"][0]
        assert "index" in choice
        assert choice["index"] == 0
        assert "message" in choice
        assert choice["message"]["role"] == "assistant"
        assert "content" in choice["message"]
        assert len(choice["message"]["content"]) > 0
        assert "finish_reason" in choice
        assert choice["finish_reason"] == "stop"

        # Check usage
        assert "usage" in data
        assert "prompt_tokens" in data["usage"]
        assert "completion_tokens" in data["usage"]
        assert "total_tokens" in data["usage"]

    def test_chat_alternative_endpoint(self, client, mock_env):
        """Test POST /chat/completions also works (without /v1 prefix)"""
        request_data = {
            "model": "mistral-large",
            "messages": [{"role": "user", "content": "Hello"}],
            "stream": False,
        }

        response = client.post("/chat/completions", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["object"] == "chat.completion"

    def test_chat_validation_error(self, client, mock_env):
        """Test chat completions with missing required fields"""
        request_data = {
            "model": "mistral-large"
            # Missing 'messages' field
        }

        response = client.post("/v1/chat/completions", json=request_data)
        assert response.status_code == 422  # Validation error


class TestCORS:
    """Test CORS configuration"""

    def test_cors_headers(self, client, mock_env):
        """Test that CORS headers are set correctly"""
        response = client.options(
            "/v1/models",
            headers={"Origin": "http://localhost:3000", "Access-Control-Request-Method": "GET"},
        )

        # CORS should be configured
        assert "access-control-allow-origin" in response.headers or response.status_code == 200
