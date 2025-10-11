"""Integration tests with real OpenAI API.

These tests actually call OpenAI and cost money!
Run only when you want to verify end-to-end functionality.

Last updated: 2025-09-21 - Added GitHub Actions integration
"""

import os
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import pytest
from openai import OpenAI

from simple_llm_request import main as cli_main
from streamlit_app import generate_poem, get_client


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

        # Test poem generation
        result = generate_poem(client, "coffee morning")

        # Verify basic structure
        assert isinstance(result, str)
        assert len(result) > 10  # Should be substantial
        paragraphs = [p for p in result.split("\n\n") if p.strip()]
        assert len(paragraphs) == 2  # Should have 2 paragraphs

        # Verify content relevance (basic check)
        result_lower = result.lower()
        # Check for any coffee-related or morning-related words
        coffee_words = [
            "coffee",
            "morning",
            "brew",
            "cup",
            "wake",
            "dawn",
            "sunrise",
            "steam",
            "aroma",
            "caffeine",
        ]
        morning_words = [
            "morning",
            "dawn",
            "sunrise",
            "wake",
            "awake",
            "early",
            "daybreak",
        ]

        # Should contain at least one relevant word
        assert any(
            word in result_lower for word in coffee_words + morning_words
        ), f"Poem should contain coffee/morning related words. Got: {result[:100]}..."

        print(f"Generated poem: {result}")

    def test_cli_openai_integration(self):
        """Test CLI with real OpenAI API."""
        with patch("builtins.input", return_value="mountain sunset"):
            with redirect_stdout(StringIO()) as captured_output:
                cli_main()

        output = captured_output.getvalue()

        # Verify output format
        assert "Generated poem:" in output

        # Check that poem was generated
        poem_blocks = [
            block
            for block in output.strip().split("\n\n")
            if block and not block.startswith("Generated poem:")
        ]
        assert len(poem_blocks) >= 1, f"Expected poem paragraphs, got: {poem_blocks}"

        print(f"CLI generated: {poem_blocks}")

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

        subjects = ["winter snow", "summer rain", "autumn leaves", "spring flowers"]

        for subject in subjects:
            result = generate_poem(client, subject)

            # Basic validation
            assert len([p for p in result.split("\n\n") if p.strip()]) == 2
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

        paragraphs = [p for p in result.split("\n\n") if p.strip()]

        # Check paragraph lengths
        paragraph_lengths = [len(paragraph.split()) for paragraph in paragraphs]

        assert len(paragraphs) == 2
        assert all(length > 5 for length in paragraph_lengths)
        assert all(length < 120 for length in paragraph_lengths)

        # Check for poetic elements
        result_lower = result.lower()
        poetic_words = ["waves", "ocean", "sea", "blue", "deep", "flow", "tide"]
        has_poetic_elements = any(word in result_lower for word in poetic_words)

        print(f"Poem: {result}")
        print(f"Paragraph lengths: {paragraph_lengths}")
        print(f"Has poetic elements: {has_poetic_elements}")


# Pytest markers for different test types
pytestmark = [
    pytest.mark.integration,  # Mark as integration test
    pytest.mark.slow,  # Mark as slow test
    pytest.mark.expensive,  # Mark as expensive test
]
