"""Unit tests for LLMService"""

from unittest.mock import MagicMock, patch

import pytest

from src.services.llm_service import LLMService


class TestLLMServiceInitialization:
    """Test LLMService initialization and validation"""

    def test_init_with_default_provider(self, mock_env, mock_mistral_model):
        """Test initialization with default provider"""
        service = LLMService()
        assert service.provider == "mistral"
        assert service._agents == {}

    def test_init_with_custom_provider(self, mock_env, mock_mistral_model):
        """Test initialization with custom provider"""
        service = LLMService(provider="mistral")
        assert service.provider == "mistral"

    def test_init_with_invalid_provider(self, mock_env, mock_mistral_model):
        """Test initialization with unsupported provider"""
        service = LLMService(provider="unsupported_provider")
        # Should not fail on init, only when trying to get model
        with pytest.raises(ValueError, match="Unsupported provider"):
            service._get_model_instance("test-model")


class TestLLMServiceModelManagement:
    """Test model instance and agent management"""

    def test_get_model_instance_mistral(self, mock_env, mock_mistral_model):
        """Test getting Mistral model instance"""
        service = LLMService(provider="mistral")
        service._get_model_instance("mistral-large")
        mock_mistral_model.assert_called_once()

    def test_get_model_instance_with_mapping(self, mock_env, mock_mistral_model):
        """Test model name mapping from config"""
        service = LLMService(provider="mistral")
        service._get_model_instance("mistral-large")
        # Should use MODEL_MAP to get "mistral-large-latest"
        mock_mistral_model.assert_called_with("mistral-large-latest")

    def test_get_model_instance_without_mapping(self, mock_env, mock_mistral_model):
        """Test model without mapping uses original name"""
        service = LLMService(provider="mistral")
        service._get_model_instance("custom-model")
        mock_mistral_model.assert_called_with("custom-model")

    def test_agent_caching(self, mock_env):
        """Test that agents are cached per provider:model"""
        with patch("src.services.llm_service.Agent") as mock_agent_class:
            # Create unique agent instances for each call
            agent1_instance = MagicMock(name="agent1")
            agent2_instance = MagicMock(name="agent2")
            mock_agent_class.side_effect = [agent1_instance, agent2_instance]

            service = LLMService(provider="mistral")

            agent1 = service._get_agent("mistral-large")
            agent2 = service._get_agent("mistral-large")
            agent3 = service._get_agent("mistral-medium")

            # Same model should return cached agent
            assert agent1 is agent2
            # Different model should create new agent
            assert agent1 is not agent3

            # Agent class should be called twice (once for each unique model)
            assert mock_agent_class.call_count == 2


class TestLLMServiceGeneration:
    """Test text generation methods"""

    @pytest.mark.asyncio
    async def test_generate_completion_single_message(
        self, mock_env, mock_agent_class, mock_agent, sample_single_message
    ):
        """Test non-streaming completion with single message"""
        service = LLMService(provider="mistral")

        result = await service.generate_completion(
            messages=sample_single_message, model="mistral-large", temperature=0.7, max_tokens=4096
        )

        assert result == "Mocked LLM response"
        mock_agent.run.assert_called_once()

        # Check that prompt was extracted correctly
        call_args = mock_agent.run.call_args
        assert call_args[0][0] == "Tell me a joke"
        assert call_args[1]["model_settings"]["temperature"] == 0.7
        assert call_args[1]["model_settings"]["max_tokens"] == 4096

    @pytest.mark.asyncio
    async def test_generate_completion_multiple_messages(
        self, mock_env, mock_agent_class, mock_agent, sample_chat_messages
    ):
        """Test non-streaming completion with conversation history"""
        service = LLMService(provider="mistral")

        result = await service.generate_completion(
            messages=sample_chat_messages, model="mistral-large", temperature=0.5, max_tokens=2000
        )

        assert result == "Mocked LLM response"

        # Check that messages were concatenated
        call_args = mock_agent.run.call_args
        prompt = call_args[0][0]
        assert "user: Hello!" in prompt
        assert "assistant: Hi there!" in prompt
        assert "user: How are you?" in prompt

    @pytest.mark.asyncio
    async def test_stream_completion_single_message(
        self, mock_env, mock_agent_class, mock_agent, sample_single_message
    ):
        """Test streaming completion"""
        service = LLMService(provider="mistral")

        chunks = []
        async for chunk in service.stream_completion(
            messages=sample_single_message, model="mistral-large", temperature=0.8, max_tokens=1000
        ):
            chunks.append(chunk)

        assert chunks == ["Hello", " ", "World", "!"]
        mock_agent.run_stream.assert_called_once()

    @pytest.mark.asyncio
    async def test_stream_completion_error_handling(self, mock_env, sample_single_message):
        """Test streaming error handling"""
        # Create agent that raises exception
        with patch("src.services.llm_service.Agent") as mock_agent_class:
            error_agent = MagicMock()
            error_agent.run_stream.side_effect = Exception("API Error")
            mock_agent_class.return_value = error_agent

            service = LLMService(provider="mistral")

            chunks = []
            async for chunk in service.stream_completion(
                messages=sample_single_message, model="mistral-large"
            ):
                chunks.append(chunk)

            assert len(chunks) == 1
            assert "Error: API Error" in chunks[0]

    @pytest.mark.asyncio
    async def test_custom_parameters(
        self, mock_env, mock_agent_class, mock_agent, sample_single_message
    ):
        """Test generation with custom temperature and max_tokens"""
        service = LLMService(provider="mistral")

        await service.generate_completion(
            messages=sample_single_message, model="mistral-large", temperature=0.3, max_tokens=500
        )

        call_args = mock_agent.run.call_args
        assert call_args[1]["model_settings"]["temperature"] == 0.3
        assert call_args[1]["model_settings"]["max_tokens"] == 500


class TestLLMServiceProviderValidation:
    """Test provider validation logic"""

    def test_validate_mistral_provider(self, mock_env, mock_mistral_model):
        """Test Mistral provider validation passes with API key"""
        service = LLMService(provider="mistral")
        # Should not raise
        service._validate_provider()
