"""Integration tests for the haiku generator."""

import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import Mock, patch

import pytest

from haiku_service import MissingAPIKeyError
from simple_llm_request import main
from streamlit_app import _poem_lines, generate_poem

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestIntegration:
    """Integration tests for the haiku generator."""

    def test_cli_and_streamlit_consistency(self, mock_env_vars, sample_subject):
        """Test that CLI and Streamlit generate consistent prompts."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[
            0
        ].message.content = "Test haiku line 1\nTest haiku line 2\nTest haiku line 3"

        # Test CLI prompt generation
        with patch("haiku_service.get_client", return_value=mock_client):
            mock_client.chat.completions.create.return_value = mock_response

            with patch("builtins.input", return_value=sample_subject):
                with patch("builtins.print"):  # Suppress output
                    main()

            cli_call = mock_client.chat.completions.create.call_args

        # Reset mock
        mock_client.reset_mock()

        # Test Streamlit prompt generation
        mock_client.chat.completions.create.return_value = mock_response

        generate_poem(mock_client, sample_subject)

        streamlit_call = mock_client.chat.completions.create.call_args

        # Compare the prompts
        cli_prompt = cli_call[1]["messages"][0]["content"]
        streamlit_prompt = streamlit_call[1]["messages"][0]["content"]

        # Both should contain the same key elements
        assert sample_subject in cli_prompt
        assert sample_subject in streamlit_prompt
        assert "haiku" in cli_prompt.lower()
        assert "haiku" in streamlit_prompt.lower()
        assert "5-7-5" in cli_prompt
        assert "5-7-5" in streamlit_prompt
        assert "three lines" in cli_prompt
        assert "three lines" in streamlit_prompt

    def test_poem_parsing_consistency(self):
        """Test that poem parsing works consistently across formats."""
        test_haikus = [
            "Line one\nLine two\nLine three",
            "Line one\n\nLine two\nLine three",
            "  Line one  \n  Line two  \n  Line three  ",
            "Line one\n   \nLine two\n\nLine three",
        ]

        for haiku in test_haikus:
            result = _poem_lines(haiku)

            # Should always return exactly 3 lines
            assert len(result) == 3, f"Failed for haiku: {repr(haiku)}"

            # Lines should be trimmed
            for line in result:
                assert line == line.strip(), "Lines should be trimmed"

            # Should not contain empty lines
            assert "" not in result, "Should not contain empty lines"

    def test_error_handling_consistency(self):
        """Test that both interfaces handle errors consistently."""
        error_message = (
            "OPENAI_API_KEY not set; add it to .env or export it before running "
            "this script."
        )

        # Test CLI error handling
        with patch(
            "haiku_service.get_client",
            side_effect=MissingAPIKeyError(error_message),
        ):
            with patch("builtins.input", return_value="test"):
                with redirect_stdout(StringIO()) as captured_output:
                    result = main()
                    assert result == 1
                    output = captured_output.getvalue()
                    assert "Error:" in output
                    assert "OPENAI_API_KEY" in output

        # Test Streamlit error handling
        with patch("streamlit_app.st") as mock_st:
            mock_st.error.return_value = None
            mock_st.stop.side_effect = SystemExit("API key not found")

            with patch(
                "haiku_service.get_client",
                side_effect=MissingAPIKeyError(error_message),
            ):
                with pytest.raises(SystemExit):
                    from streamlit_app import get_client

                    get_client()

            mock_st.error.assert_called_once()
            mock_st.stop.assert_called_once()

    def test_model_consistency(self, mock_env_vars, sample_subject):
        """Test that both interfaces use the same model."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = "Test haiku"

        # Test CLI model
        with patch("haiku_service.get_client", return_value=mock_client):
            mock_client.chat.completions.create.return_value = mock_response

            with patch("builtins.input", return_value=sample_subject):
                with patch("builtins.print"):
                    main()

            cli_model = mock_client.chat.completions.create.call_args[1]["model"]

        # Reset mock
        mock_client.reset_mock()

        # Test Streamlit model
        mock_client.chat.completions.create.return_value = mock_response

        generate_poem(mock_client, sample_subject)

        streamlit_model = mock_client.chat.completions.create.call_args[1]["model"]

        # Both should use the same model
        assert cli_model == streamlit_model
        assert cli_model == "gpt-4o-mini"

    def test_environment_variable_handling(self):
        """Test that both interfaces handle environment variables consistently."""
        test_key = "test-api-key-123"

        # Test CLI
        with patch.dict(os.environ, {"OPENAI_API_KEY": test_key}):
            with patch("haiku_service.OpenAI") as mock_openai_class:
                mock_client = Mock()
                mock_openai_class.return_value = mock_client

                with patch("builtins.input", return_value="test"):
                    with patch("builtins.print"):
                        main()

                mock_openai_class.assert_called_once_with(api_key=test_key)

        # Test Streamlit
        with patch.dict(os.environ, {"OPENAI_API_KEY": test_key}):
            with patch("haiku_service.OpenAI") as mock_openai_class:
                mock_client = Mock()
                mock_openai_class.return_value = mock_client

                from streamlit_app import get_client

                get_client()

                mock_openai_class.assert_called_once_with(api_key=test_key)
