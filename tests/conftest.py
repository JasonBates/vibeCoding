"""Pytest configuration and fixtures for haiku generator tests."""

import os
from unittest.mock import Mock, patch

import pytest
from openai import OpenAI


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    client = Mock(spec=OpenAI)
    return client


@pytest.fixture
def mock_api_response():
    """Mock API response for haiku generation."""
    response = Mock()
    response.output_text = (
        "Silent mind explored\nBound in trials of unknown\nTruth in quiet waits"
    )
    return response


@pytest.fixture
def sample_haiku():
    """Sample haiku for testing formatting."""
    return "Silent mind explored\nBound in trials of unknown\nTruth in quiet waits"


@pytest.fixture
def sample_subject():
    """Sample subject for testing."""
    return "coffee morning"


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-api-key"}):
        yield
