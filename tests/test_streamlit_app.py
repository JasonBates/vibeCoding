"""Tests for the Streamlit haiku generator app."""

import os
import sys
from unittest.mock import Mock, patch

import pytest

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streamlit_app import _poem_lines, generate_poem, get_client


class TestStreamlitApp:
    """Test cases for Streamlit app functionality."""

    def test_get_client_with_valid_key(self, mock_env_vars):
        """Test get_client with valid API key."""
        with patch("streamlit_app.OpenAI") as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client

            client = get_client()

            assert client == mock_client
            mock_openai_class.assert_called_once_with(api_key="test-api-key")

    def test_get_client_without_api_key(self):
        """Test get_client without API key raises error."""
        with patch.dict(os.environ, {}, clear=True):
            with patch(
                "streamlit_app.load_dotenv"
            ):  # Mock load_dotenv to prevent .env loading
                with patch("streamlit_app.st") as mock_st:
                    mock_st.error.return_value = None
                    mock_st.stop.side_effect = SystemExit("API key not found")

                    with pytest.raises(SystemExit):  # st.stop() raises SystemExit
                        get_client()

                    mock_st.error.assert_called_once()
                    mock_st.stop.assert_called_once()

    def test_generate_poem(self, mock_openai_client, mock_api_response, sample_subject):
        """Test generate_poem function."""
        mock_openai_client.responses.create.return_value = mock_api_response

        result = generate_poem(mock_openai_client, sample_subject)

        # Verify API call
        mock_openai_client.responses.create.assert_called_once()
        call_args = mock_openai_client.responses.create.call_args

        assert call_args[1]["model"] == "gpt-4.1-mini"
        assert sample_subject in call_args[1]["input"]
        assert "haiku" in call_args[1]["input"].lower()
        assert "5-7-5" in call_args[1]["input"]
        assert "Return the haiku as three lines" in call_args[1]["input"]

        # Verify return value
        assert result == mock_api_response.output_text

    def test_poem_lines_with_newlines(self, sample_haiku):
        """Test _poem_lines with newline-separated haiku."""
        result = _poem_lines(sample_haiku)

        expected = [
            "Silent mind explored",
            "Bound in trials of unknown",
            "Truth in quiet waits",
        ]
        assert result == expected

    def test_poem_lines_with_empty_lines(self):
        """Test _poem_lines with empty lines."""
        haiku_with_empty = "Line one\n\nLine two\n   \nLine three"
        result = _poem_lines(haiku_with_empty)

        expected = ["Line one", "Line two", "Line three"]
        assert result == expected

    def test_poem_lines_with_single_line(self):
        """Test _poem_lines with single line (fallback)."""
        single_line = "This is a single line haiku"
        result = _poem_lines(single_line)

        assert result == [single_line]

    def test_poem_lines_with_empty_input(self):
        """Test _poem_lines with empty input."""
        result = _poem_lines("")
        assert result == [""]

    def test_poem_lines_with_whitespace_only(self):
        """Test _poem_lines with whitespace-only lines."""
        haiku_with_whitespace = "Line one\n   \n  \nLine two"
        result = _poem_lines(haiku_with_whitespace)

        expected = ["Line one", "Line two"]
        assert result == expected

    def test_generate_poem_prompt_formatting(
        self, mock_openai_client, mock_api_response
    ):
        """Test that generate_poem creates correct prompt format."""
        test_subject = "mountain peaks"
        mock_openai_client.responses.create.return_value = mock_api_response

        generate_poem(mock_openai_client, test_subject)

        call_args = mock_openai_client.responses.create.call_args
        prompt = call_args[1]["input"]

        # Check prompt components
        assert "Write an English haiku" in prompt
        assert "three lines, 5-7-5 syllable pattern" in prompt
        assert f"about the following subject: {test_subject}." in prompt
        assert "Return the haiku as three lines" in prompt
        assert "each line on its own line" in prompt
