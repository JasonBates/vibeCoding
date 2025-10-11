"""Tests for poem validation and formatting."""

import os
import sys

import pytest

from streamlit_app import _poem_paragraphs

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPoemValidation:
    """Test cases for poem validation and formatting."""

    def test_paragraph_count(self, sample_haiku):
        """Test that generated poem has exactly two paragraphs."""
        paragraphs = _poem_paragraphs(sample_haiku)
        assert (
            len(paragraphs) == 2
        ), f"Expected 2 paragraphs, got {len(paragraphs)}: {paragraphs}"

    def test_paragraph_sentence_count(self, sample_haiku):
        """Test that each paragraph includes at least three sentences."""
        paragraphs = _poem_paragraphs(sample_haiku)

        for paragraph in paragraphs:
            sentences = [part for part in paragraph.split(".") if part.strip()]
            assert len(sentences) >= 3, (
                "Each paragraph should contain multiple sentences; "
                f"got {len(sentences)} in paragraph {paragraph!r}"
            )

    def test_poem_has_blank_line_separator(self, sample_haiku):
        """Test that poem uses a blank line to separate paragraphs."""
        assert "\n\n" in sample_haiku
        paragraphs = _poem_paragraphs(sample_haiku)
        assert len(paragraphs) == 2

    def test_poem_no_pipe_separators(self, sample_haiku):
        """Test that poem doesn't contain pipe separators."""
        assert "|" not in sample_haiku
        paragraphs = _poem_paragraphs(sample_haiku)
        for paragraph in paragraphs:
            assert "|" not in paragraph

    def test_poem_paragraph_handling(self):
        """Test _poem_paragraphs handles various input formats."""
        test_cases = [
            (
                "Paragraph one sentence. Another sentence. Third sentence.\n\n"
                "Paragraph two sentence. Extra idea. Closing line.",
                [
                    "Paragraph one sentence. Another sentence. Third sentence.",
                    "Paragraph two sentence. Extra idea. Closing line.",
                ],
            ),
            (
                "Paragraph one sentence.\n\n\nParagraph two sentence.",
                [
                    "Paragraph one sentence.",
                    "Paragraph two sentence.",
                ],
            ),
            ("Single paragraph only", ["Single paragraph only"]),
            ("", [""]),
        ]

        for input_text, expected in test_cases:
            result = _poem_paragraphs(input_text)
            assert result == expected, f"Failed for input: {repr(input_text)}"

    def test_poem_content_quality(self, sample_haiku):
        """Test basic content quality of generated poem."""
        paragraphs = _poem_paragraphs(sample_haiku)

        for paragraph in paragraphs:
            assert len(paragraph.strip()) > 0
            assert len(paragraph.split()) > 3

        assert len(set(paragraphs)) > 1, "Paragraphs should provide distinct imagery"

        all_text = " ".join(paragraphs)
        words = all_text.split()
        assert len(words) >= 15, "Poem should have a reasonable word count"

    def test_poem_trimming(self):
        """Test that _poem_paragraphs properly trims whitespace."""
        poem_with_spaces = (
            "  First paragraph line one.  Line two.  Line three.  \n\n"
            "  Second paragraph rises.  Another thought.  Final cadence.  "
        )
        result = _poem_paragraphs(poem_with_spaces)

        expected = [
            "First paragraph line one.  Line two.  Line three.",
            "Second paragraph rises.  Another thought.  Final cadence.",
        ]
        assert result == expected

    def test_poem_empty_paragraph_removal(self):
        """Test that empty paragraphs are properly removed."""
        poem_with_empty = "Paragraph one.\n\n\n\nParagraph two."
        result = _poem_paragraphs(poem_with_empty)

        expected = ["Paragraph one.", "Paragraph two."]
        assert result == expected
