"""Tests for the CLI haiku generator."""

import io

# Add parent directory to path to import the module
import os
import sys
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import Mock, call, patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simple_llm_request import main


class TestCLI:
    """Test cases for CLI functionality."""

    def test_main_with_valid_api_key(
        self, mock_env_vars, mock_openai_client, mock_api_response
    ):
        """Test main function with valid API key."""
        with patch("simple_llm_request.OpenAI", return_value=mock_openai_client):
            mock_openai_client.responses.create.return_value = mock_api_response

            # Test with input
            with patch("builtins.input", return_value="test subject"):
                with redirect_stdout(StringIO()) as captured_output:
                    main()

            # Verify API was called correctly
            mock_openai_client.responses.create.assert_called_once()
            call_args = mock_openai_client.responses.create.call_args

            assert call_args[1]["model"] == "gpt-4.1-mini"
            assert "test subject" in call_args[1]["input"]
            assert "haiku" in call_args[1]["input"].lower()
            assert "5-7-5" in call_args[1]["input"]

            # Verify output
            output = captured_output.getvalue()
            assert "Generated haiku:" in output
            assert "Silent mind explored" in output

    def test_main_with_default_subject(
        self, mock_env_vars, mock_openai_client, mock_api_response
    ):
        """Test main function with empty input (default subject)."""
        with patch("simple_llm_request.OpenAI", return_value=mock_openai_client):
            mock_openai_client.responses.create.return_value = mock_api_response

            # Test with empty input (should use default)
            with patch("builtins.input", return_value=""):
                with redirect_stdout(StringIO()) as captured_output:
                    main()

            # Verify default subject was used
            call_args = mock_openai_client.responses.create.call_args
            assert "quiet mornings" in call_args[1]["input"]

    def test_main_without_api_key(self):
        """Test main function without API key raises error."""
        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "simple_llm_request.load_dotenv"
            ):  # Mock load_dotenv to prevent .env loading
                with patch(
                    "builtins.input", return_value="test"
                ):  # Mock input to avoid stdin issues
                    with pytest.raises(RuntimeError, match="OPENAI_API_KEY not set"):
                        main()

    def test_prompt_formatting(
        self, mock_env_vars, mock_openai_client, mock_api_response
    ):
        """Test that prompt is formatted correctly."""
        with patch("simple_llm_request.OpenAI", return_value=mock_openai_client):
            mock_openai_client.responses.create.return_value = mock_api_response

            test_subject = "ocean waves"
            with patch("builtins.input", return_value=test_subject):
                with redirect_stdout(StringIO()) as captured_output:
                    main()

            call_args = mock_openai_client.responses.create.call_args
            prompt = call_args[1]["input"]

            # Check prompt components
            assert "English haiku" in prompt
            assert "three lines" in prompt
            assert "5-7-5 syllable pattern" in prompt
            assert test_subject in prompt
            assert "Return the haiku as three lines" in prompt
            assert "each line on its own line" in prompt

    def test_output_formatting(self, mock_env_vars, mock_openai_client, sample_haiku):
        """Test that output is formatted correctly."""
        response = Mock()
        response.output_text = sample_haiku

        with patch("simple_llm_request.OpenAI", return_value=mock_openai_client):
            mock_openai_client.responses.create.return_value = response

            with patch("builtins.input", return_value="test"):
                with redirect_stdout(StringIO()) as captured_output:
                    main()

            output = captured_output.getvalue()

            # Check output format
            assert "Generated haiku:" in output
            assert "Silent mind explored" in output
            assert "Bound in trials of unknown" in output
            assert "Truth in quiet waits" in output
            # Should not contain pipe separators
            assert "|" not in output
