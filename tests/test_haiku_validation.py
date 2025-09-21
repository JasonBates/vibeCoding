"""Tests for haiku validation and formatting."""

import pytest
import re
import sys
import os

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streamlit_app import _poem_lines


class TestHaikuValidation:
    """Test cases for haiku validation and formatting."""

    def test_haiku_line_count(self, sample_haiku):
        """Test that haiku has exactly 3 lines."""
        lines = _poem_lines(sample_haiku)
        assert len(lines) == 3, f"Expected 3 lines, got {len(lines)}: {lines}"

    def test_haiku_syllable_pattern(self):
        """Test haiku syllable pattern (5-7-5)."""
        # This is a simplified test - in practice, you'd need a syllable counter
        # For now, we'll test that the lines exist and are reasonable lengths
        haiku = "Silent mind explored\nBound in trials of unknown\nTruth in quiet waits"
        lines = _poem_lines(haiku)
        
        assert len(lines) == 3
        # Basic length checks (not perfect syllable counting)
        assert len(lines[0].split()) >= 2  # First line should have some words
        assert len(lines[1].split()) >= 3  # Second line should be longer
        assert len(lines[2].split()) >= 2  # Third line should have some words

    def test_haiku_no_pipe_separators(self, sample_haiku):
        """Test that haiku doesn't contain pipe separators."""
        assert "|" not in sample_haiku
        lines = _poem_lines(sample_haiku)
        for line in lines:
            assert "|" not in line

    def test_haiku_uses_newlines(self, sample_haiku):
        """Test that haiku uses newlines for separation."""
        assert "\n" in sample_haiku
        lines = _poem_lines(sample_haiku)
        assert len(lines) > 1

    def test_poem_lines_handles_various_formats(self):
        """Test _poem_lines handles various input formats."""
        test_cases = [
            ("Line1\nLine2\nLine3", ["Line1", "Line2", "Line3"]),
            ("Line1\n\nLine2\nLine3", ["Line1", "Line2", "Line3"]),
            ("Line1\n   \nLine2", ["Line1", "Line2"]),
            ("Single line", ["Single line"]),
            ("", [""]),
        ]
        
        for input_text, expected in test_cases:
            result = _poem_lines(input_text)
            assert result == expected, f"Failed for input: {repr(input_text)}"

    def test_haiku_content_quality(self, sample_haiku):
        """Test basic content quality of generated haiku."""
        lines = _poem_lines(sample_haiku)
        
        # Each line should have content
        for line in lines:
            assert len(line.strip()) > 0
            assert len(line.split()) > 0  # Should have words
        
        # Should not be identical lines
        assert len(set(lines)) > 1, "All lines should not be identical"
        
        # Should contain some meaningful words (not just punctuation)
        all_text = " ".join(lines)
        words = all_text.split()
        assert len(words) >= 6, "Haiku should have reasonable word count"

    def test_haiku_trimming(self):
        """Test that _poem_lines properly trims whitespace."""
        haiku_with_spaces = "  Line one  \n  Line two  \n  Line three  "
        result = _poem_lines(haiku_with_spaces)
        
        expected = ["Line one", "Line two", "Line three"]
        assert result == expected

    def test_haiku_empty_lines_removal(self):
        """Test that empty lines are properly removed."""
        haiku_with_empty = "Line one\n\n\nLine two\n\nLine three"
        result = _poem_lines(haiku_with_empty)
        
        expected = ["Line one", "Line two", "Line three"]
        assert result == expected
