"""Tests for the CLI poem generator."""

import io

# Add parent directory to path to import the module
import os
import sys
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import Mock, patch

import pytest

from haiku_service import MissingAPIKeyError
from simple_llm_request import main

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCLI:
    """Test cases for CLI functionality."""

    def test_main_with_valid_api_key(self, mock_env_vars, mock_openai_client, mock_api_response):
        """Test main function with valid API key."""
        with patch("haiku_service.get_client", return_value=mock_openai_client):
            mock_openai_client.chat.completions.create.return_value = mock_api_response

            # Test with input
            with patch("builtins.input", return_value="test subject"):
                with redirect_stdout(StringIO()) as captured_output:
                    main()

            # Verify API was called correctly
            mock_openai_client.chat.completions.create.assert_called_once()
            call_args = mock_openai_client.chat.completions.create.call_args

            assert call_args[1]["model"] == "gpt-4o-mini"
            assert "test subject" in call_args[1]["messages"][0]["content"]
            prompt_content = call_args[1]["messages"][0]["content"].lower()
            assert "poem" in prompt_content
            assert "two distinct paragraphs" in prompt_content
            assert "blank line" in prompt_content

            # Verify output
            output = captured_output.getvalue()
            assert "Generated poem:" in output
            assert "Silent mind explored" in output

    def test_main_with_default_subject(self, mock_env_vars, mock_openai_client, mock_api_response):
        """Test main function with empty input (default subject)."""
        with patch("haiku_service.get_client", return_value=mock_openai_client):
            mock_openai_client.chat.completions.create.return_value = mock_api_response

            # Test with empty input (should use default)
            with patch("builtins.input", return_value=""):
                with redirect_stdout(StringIO()) as captured_output:
                    main()

            # Verify default subject was used
            call_args = mock_openai_client.chat.completions.create.call_args
            assert "quiet mornings" in call_args[1]["messages"][0]["content"]

    def test_main_without_api_key(self):
        """Test main function without API key returns error code."""
        error_message = "OPENAI_API_KEY not set; add it to .env or export it before running " "this script."

        with patch(
            "haiku_service.get_client",
            side_effect=MissingAPIKeyError(error_message),
        ):
            with patch("builtins.input", return_value="test"):  # Mock input to avoid stdin issues
                with redirect_stdout(StringIO()) as captured_output:
                    result = main()
                    assert result == 1
                    output = captured_output.getvalue()
                    assert "Error:" in output
                    assert "OPENAI_API_KEY" in output

    def test_prompt_formatting(self, mock_env_vars, mock_openai_client, mock_api_response):
        """Test that prompt is formatted correctly."""
        with patch("haiku_service.get_client", return_value=mock_openai_client):
            mock_openai_client.chat.completions.create.return_value = mock_api_response

            test_subject = "ocean waves"
            with patch("builtins.input", return_value=test_subject):
                with redirect_stdout(StringIO()) as captured_output:
                    main()

            call_args = mock_openai_client.chat.completions.create.call_args
            prompt = call_args[1]["messages"][0]["content"]

            # Check prompt components
            assert "English poem" in prompt
            assert "two distinct paragraphs" in prompt
            assert "three sentences" in prompt
            assert test_subject in prompt
            assert "Return the poem as exactly two paragraphs" in prompt

    def test_output_formatting(self, mock_env_vars, mock_openai_client, sample_haiku):
        """Test that output is formatted correctly."""
        response = Mock()
        response.choices = [Mock()]
        response.choices[0].message = Mock()
        response.choices[0].message.content = sample_haiku

        with patch("haiku_service.get_client", return_value=mock_openai_client):
            mock_openai_client.chat.completions.create.return_value = response

            with patch("builtins.input", return_value="test"):
                with redirect_stdout(StringIO()) as captured_output:
                    main()

            output = captured_output.getvalue()

            # Check output format
            assert "Generated poem:" in output
            assert "Silent mind explored" in output
            assert "lavender air" in output
            assert "silver whispers" in output
            # Should not contain pipe separators
            assert "|" not in output
