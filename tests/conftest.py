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


POEM_TEXT = (
    "Silent mind explored in hush of dawn. Dreams wander through lavender air. "
    "We breathe the promise of morning.\n\n"
    "Moonlight drifts across the quiet lake. Memories ripple in silver whispers. "
    "We hold the night between our hands."
)


@pytest.fixture
def mock_api_response():
    """Mock API response for poem generation."""
    response = Mock()
    response.choices = [Mock()]
    response.choices[0].message = Mock()
    response.choices[0].message.content = POEM_TEXT
    return response


@pytest.fixture
def sample_haiku():
    """Sample poem for testing formatting."""
    return POEM_TEXT


@pytest.fixture
def sample_subject():
    """Sample subject for testing."""
    return "coffee morning"


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-api-key"}):
        yield
