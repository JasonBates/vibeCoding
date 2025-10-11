"""Tests for the Streamlit poem generator app."""

import os
import sys
from unittest.mock import Mock, patch

import pytest

from haiku_service import MissingAPIKeyError
from streamlit_app import _poem_paragraphs, generate_poem, get_client

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestStreamlitApp:
    """Test cases for Streamlit app functionality."""

    def test_get_client_with_valid_key(self, mock_env_vars):
        """Test get_client with valid API key."""
        with patch("haiku_service.get_client") as mock_get_client:
            mock_client = Mock()
            mock_get_client.return_value = mock_client

            client = get_client()

            assert client == mock_client
            mock_get_client.assert_called_once()

    def test_get_client_without_api_key(self):
        """Test get_client without API key raises error."""
        error_message = (
            "OPENAI_API_KEY not set; add it to .env or export it before running "
            "this script."
        )

        with patch("streamlit_app.st") as mock_st:
            mock_st.error.return_value = None
            mock_st.stop.side_effect = SystemExit("API key not found")

            with patch(
                "haiku_service.get_client",
                side_effect=MissingAPIKeyError(error_message),
            ):
                with pytest.raises(SystemExit):  # st.stop() raises SystemExit
                    get_client()

            mock_st.error.assert_called_once()
            mock_st.stop.assert_called_once()

    def test_generate_poem(self, mock_openai_client, mock_api_response, sample_subject):
        """Test generate_poem function."""
        mock_openai_client.chat.completions.create.return_value = mock_api_response

        result = generate_poem(mock_openai_client, sample_subject)

        # Verify API call
        mock_openai_client.chat.completions.create.assert_called_once()
        call_args = mock_openai_client.chat.completions.create.call_args

        assert call_args[1]["model"] == "gpt-4o-mini"
        assert sample_subject in call_args[1]["messages"][0]["content"]
        prompt_content = call_args[1]["messages"][0]["content"].lower()
        assert "poem" in prompt_content
        assert "two distinct paragraphs" in prompt_content
        assert "blank line" in prompt_content

        # Verify return value
        assert result == mock_api_response.choices[0].message.content

    def test_poem_paragraphs_with_blank_line(self, sample_haiku):
        """Test _poem_paragraphs with blank-line-separated paragraphs."""
        result = _poem_paragraphs(sample_haiku)

        expected = [
            "Silent mind explored in hush of dawn. Dreams wander through lavender air. We breathe the promise of morning.",
            "Moonlight drifts across the quiet lake. Memories ripple in silver whispers. We hold the night between our hands.",
        ]
        assert result == expected

    def test_poem_paragraphs_with_extra_spacing(self):
        """Test _poem_paragraphs removes empty paragraphs and trims spacing."""
        poem_with_extra = (
            " First paragraph sentence one.  Sentence two.  Sentence three. \n\n"
            "\n"
            " Second paragraph grows in moonlight. Another sentence forms. Closing thought blooms. "
        )
        result = _poem_paragraphs(poem_with_extra)

        expected = [
            "First paragraph sentence one.  Sentence two.  Sentence three.",
            "Second paragraph grows in moonlight. Another sentence forms. Closing thought blooms.",
        ]
        assert result == expected

    def test_poem_paragraphs_with_single_block(self):
        """Test _poem_paragraphs with single block (fallback)."""
        single_block = "This is a single paragraph poem"
        result = _poem_paragraphs(single_block)

        assert result == ["This is a single paragraph poem"]

    def test_poem_paragraphs_with_empty_input(self):
        """Test _poem_paragraphs with empty input."""
        result = _poem_paragraphs("")
        assert result == [""]

    def test_poem_paragraphs_with_whitespace_only(self):
        """Test _poem_paragraphs removes whitespace-only paragraphs."""
        poem_with_whitespace = "Line one\n   \n  \n\nLine two"
        result = _poem_paragraphs(poem_with_whitespace)

        expected = ["Line one", "Line two"]
        assert result == expected

    def test_generate_poem_prompt_formatting(
        self, mock_openai_client, mock_api_response
    ):
        """Test that generate_poem creates correct prompt format."""
        test_subject = "mountain peaks"
        mock_openai_client.chat.completions.create.return_value = mock_api_response

        generate_poem(mock_openai_client, test_subject)

        call_args = mock_openai_client.chat.completions.create.call_args
        prompt = call_args[1]["messages"][0]["content"]

        # Check prompt components
        assert "Write an English poem" in prompt
        assert "two distinct paragraphs" in prompt
        assert f"about the following subject: {test_subject}." in prompt
        assert "Return the poem as exactly two paragraphs" in prompt
        assert "blank line" in prompt
