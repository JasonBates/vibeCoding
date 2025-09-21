"""End-to-end tests for complete haiku generation workflow.

These tests verify the complete user journey from input to output.
"""

import os
import pytest
import subprocess
import sys
from pathlib import Path


class TestEndToEndHaiku:
    """End-to-end tests for complete haiku generation."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for E2E tests."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            pytest.skip("No OPENAI_API_KEY found - skipping E2E tests")

    def test_complete_cli_workflow(self):
        """Test complete CLI workflow from start to finish."""
        # Test the CLI script directly
        result = subprocess.run([
            sys.executable, "simple_llm_request.py"
        ], input="forest meditation\n", text=True, capture_output=True)

        # Should succeed
        assert result.returncode == 0

        # Should contain expected output
        assert "Generated haiku:" in result.stdout

        # Should have 3 lines of haiku
        lines = result.stdout.strip().split('\n')
        haiku_lines = [line for line in lines
                       if line and not line.startswith("Generated haiku:") and not line.startswith("Enter a subject")]
        assert len(
            haiku_lines) == 3, f"Expected 3 haiku lines, got {len(haiku_lines)}: {haiku_lines}"

        print(f"E2E CLI Output: {result.stdout}")

    def test_streamlit_app_imports(self):
        """Test that Streamlit app can be imported and basic functions work."""
        # Test importing the app
        import streamlit_app

        # Test that main functions exist
        assert hasattr(streamlit_app, 'generate_poem')
        assert hasattr(streamlit_app, 'get_client')
        assert hasattr(streamlit_app, 'main')

        # Test that functions are callable
        assert callable(streamlit_app.generate_poem)
        assert callable(streamlit_app.get_client)
        assert callable(streamlit_app.main)

    def test_environment_setup(self):
        """Test that environment is properly set up for the app."""
        # Check required environment variables
        assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not set"

        # Check that .env file exists (if used)
        env_file = Path(".env")
        if env_file.exists():
            assert env_file.is_file()
            print(f".env file exists: {env_file.absolute()}")

        # Check that required Python packages are available
        try:
            import openai
            import streamlit
            import dotenv
            print("All required packages are available")
        except ImportError as e:
            pytest.fail(f"Missing required package: {e}")

    def test_haiku_generation_consistency(self):
        """Test that haiku generation is consistent between runs."""
        from streamlit_app import generate_poem, get_client

        client = get_client()
        subject = "moonlight reflection"

        # Generate multiple haikus with same subject
        results = []
        for i in range(3):
            result = generate_poem(client, subject)
            results.append(result)
            print(f"Run {i+1}: {result}")

        # All should be valid haikus
        for result in results:
            lines = result.split('\n')
            assert len(
                lines) == 3, f"Expected 3 lines, got {len(lines)}: {result}"
            assert all(line.strip()
                       for line in lines), f"Empty lines found: {result}"

        # They should be different (creativity test)
        unique_results = set(results)
        assert len(
            unique_results) > 1, "All haikus were identical - lack of creativity"

        print(
            f"Generated {len(unique_results)} unique haikus out of {len(results)} runs")

    def test_error_handling_e2e(self):
        """Test error handling in complete workflow."""
        # Test with empty input
        result = subprocess.run([
            sys.executable, "simple_llm_request.py"
        ], input="\n", text=True, capture_output=True)

        # Should still succeed (uses default subject)
        assert result.returncode == 0
        assert "Generated haiku:" in result.stdout

        print(f"Empty input test: {result.stdout}")


# Pytest markers for E2E tests
pytestmark = [
    pytest.mark.integration,  # Mark as integration test
    pytest.mark.e2e,         # Mark as end-to-end test
    pytest.mark.slow,        # Mark as slow test
    pytest.mark.expensive,   # Mark as expensive test
]
