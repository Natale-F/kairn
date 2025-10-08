"""Pytest configuration and shared fixtures"""

import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def mock_env():
    """Mock environment variables for testing"""
    env_vars = {
        "MISTRAL_API_KEY": "test_mistral_key_12345",
        "LLM_PROVIDER": "mistral",
        "FRONTEND_URL": "http://localhost:3000",
    }

    with patch.dict(os.environ, env_vars):
        yield env_vars


@pytest.fixture
def mock_agent():
    """Mock Pydantic AI Agent"""
    mock = MagicMock()

    # Mock run() for non-streaming
    mock_result = MagicMock()
    mock_result.data = "Mocked LLM response"
    mock.run = AsyncMock(return_value=mock_result)

    # Mock run_stream() for streaming
    class MockStreamResponse:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def stream_text(self, delta=False):
            """Stream text chunks"""
            chunks = ["Hello", " ", "World", "!"]
            for chunk in chunks:
                yield chunk

    mock.run_stream = MagicMock(return_value=MockStreamResponse())

    return mock


@pytest.fixture
def mock_agent_class(mock_agent):
    """Mock Agent class to return our mock agent"""
    with patch("src.services.llm_service.Agent") as mock_class:
        mock_class.return_value = mock_agent
        yield mock_class


@pytest.fixture
def mock_mistral_model():
    """Mock MistralModel for testing"""
    with patch("src.services.llm_service.MistralModel") as mock:
        yield mock


@pytest.fixture
def mock_llm_service(mock_agent):
    """Mock LLMService for API tests"""
    with patch("src.api.ollama_routes.LLMService") as mock_service_class:
        mock_instance = MagicMock()
        mock_instance.generate_completion = mock_agent.run
        mock_instance.stream_completion = mock_agent.run_stream().stream_text
        mock_service_class.return_value = mock_instance
        yield mock_service_class


@pytest.fixture
def client(mock_env, mock_llm_service):
    """FastAPI test client with mocked LLM"""
    # Import after mocking to ensure mocks are in place
    from src.main import app

    return TestClient(app)


@pytest.fixture
def sample_chat_messages():
    """Sample chat messages for testing"""
    return [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there!"},
        {"role": "user", "content": "How are you?"},
    ]


@pytest.fixture
def sample_single_message():
    """Single message for testing"""
    return [{"role": "user", "content": "Tell me a joke"}]
