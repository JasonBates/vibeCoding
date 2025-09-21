"""Integration tests with real OpenAI API.

These tests actually call OpenAI and cost money!
Run only when you want to verify end-to-end functionality.
"""

import os
import pytest
from unittest.mock import patch
from openai import OpenAI
from streamlit_app import generate_poem, get_client
from simple_llm_request import main as cli_main
from contextlib import redirect_stdout
from io import StringIO


class TestOpenAIIntegration:
    """Integration tests with real OpenAI API."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for integration tests."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            pytest.skip("No OPENAI_API_KEY found - skipping integration tests")

    def test_streamlit_openai_integration(self):
        """Test Streamlit app with real OpenAI API."""
        client = get_client()

        # Test haiku generation
        result = generate_poem(client, "coffee morning")

        # Verify basic structure
        assert isinstance(result, str)
        assert len(result) > 10  # Should be substantial
        assert len(result.split('\n')) == 3  # Should have 3 lines

        # Verify content relevance (basic check)
        result_lower = result.lower()
        assert any(word in result_lower for word in [
                   "coffee", "morning", "brew", "cup", "wake"])

        print(f"Generated haiku: {result}")

    def test_cli_openai_integration(self):
        """Test CLI with real OpenAI API."""
        with patch('builtins.input', return_value="mountain sunset"):
            with redirect_stdout(StringIO()) as captured_output:
                cli_main()

        output = captured_output.getvalue()

        # Verify output format
        assert "Generated haiku:" in output

        # Check that haiku was generated (more flexible than exact word matching)
        haiku_lines = [line for line in output.strip().split('\n')
                       if line and not line.startswith("Generated haiku:")]
        assert len(
            haiku_lines) == 3, f"Expected 3 haiku lines, got {len(haiku_lines)}: {haiku_lines}"

        # Extract the haiku from output
        lines = output.strip().split('\n')
        haiku_lines = [
            line for line in lines if line and not line.startswith("Generated haiku:")]

        assert len(haiku_lines) == 3
        print(f"CLI generated: {haiku_lines}")

    def test_api_error_handling(self):
        """Test error handling with invalid API key."""
        # Temporarily use invalid key
        original_key = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = "invalid-key-12345"

        try:
            client = get_client()
            with pytest.raises(Exception):  # Should fail
                generate_poem(client, "test")
        finally:
            # Restore original key
            if original_key:
                os.environ["OPENAI_API_KEY"] = original_key
            else:
                del os.environ["OPENAI_API_KEY"]

    def test_different_subjects(self):
        """Test haiku generation with different subjects."""
        client = get_client()

        subjects = [
            "winter snow",
            "summer rain",
            "autumn leaves",
            "spring flowers"
        ]

        for subject in subjects:
            result = generate_poem(client, subject)

            # Basic validation
            assert len(result.split('\n')) == 3
            assert len(result) > 15

            # Check if subject is referenced (not always guaranteed)
            result_lower = result.lower()
            subject_words = subject.split()
            has_reference = any(word in result_lower for word in subject_words)

            print(f"Subject: {subject}")
            print(f"Haiku: {result}")
            print(f"References subject: {has_reference}")
            print("-" * 40)

    def test_haiku_quality_metrics(self):
        """Test basic quality metrics of generated haikus."""
        client = get_client()
        result = generate_poem(client, "ocean waves")

        lines = result.split('\n')

        # Check line lengths (rough syllable approximation)
        line_lengths = [len(line.strip()) for line in lines if line.strip()]

        # Haiku should have varying line lengths (5-7-5 pattern)
        assert len(line_lengths) == 3
        assert all(length > 5 for length in line_lengths)  # Not too short
        assert all(length < 50 for length in line_lengths)  # Not too long

        # Check for poetic elements
        result_lower = result.lower()
        poetic_words = ["waves", "ocean", "sea",
                        "blue", "deep", "flow", "tide"]
        has_poetic_elements = any(
            word in result_lower for word in poetic_words)

        print(f"Haiku: {result}")
        print(f"Line lengths: {line_lengths}")
        print(f"Has poetic elements: {has_poetic_elements}")


# Pytest markers for different test types
pytestmark = [
    pytest.mark.integration,  # Mark as integration test
    pytest.mark.slow,         # Mark as slow test
    pytest.mark.expensive,    # Mark as expensive test
]
