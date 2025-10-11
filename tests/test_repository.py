"""Tests for the haiku repository layer."""
from __future__ import annotations

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from models import Haiku
from repository import HaikuRepository


class TestHaikuRepository:
    """Test cases for HaikuRepository."""

    @pytest.fixture
    def mock_supabase_client(self):
        """Mock Supabase client for testing."""
        client = Mock()
        client.table.return_value = Mock()
        return client

    @pytest.fixture
    def repository(self, mock_supabase_client):
        """Create repository instance with mocked client."""
        return HaikuRepository(mock_supabase_client)

    @pytest.fixture
    def sample_haiku(self):
        """Sample haiku for testing."""
        return Haiku(
            subject="coffee morning",
            haiku_text="Silent mind explored\nBound in trials of unknown\nTruth in quiet waits",
            id="test-id-123",
            created_at=datetime(2024, 1, 15, 10, 30, 0),
            user_id="user-123",
        )

    def test_save_haiku_success(self, repository, sample_haiku, mock_supabase_client):
        """Test successful haiku saving."""
        # Mock the Supabase response
        mock_table = Mock()
        mock_insert = Mock()
        mock_execute = Mock()

        mock_execute.data = [sample_haiku.to_dict()]
        mock_insert.execute.return_value = mock_execute
        mock_table.insert.return_value = mock_insert
        mock_supabase_client.table.return_value = mock_table

        # Test save
        result = repository.save(sample_haiku)

        # Verify calls
        mock_supabase_client.table.assert_called_once_with("haikus")
        mock_table.insert.assert_called_once()
        mock_insert.execute.assert_called_once()

        # Verify result
        assert isinstance(result, Haiku)
        assert result.subject == sample_haiku.subject
        assert result.haiku_text == sample_haiku.haiku_text

    def test_save_haiku_failure(self, repository, sample_haiku, mock_supabase_client):
        """Test haiku saving failure."""
        # Mock the Supabase response to fail
        mock_table = Mock()
        mock_insert = Mock()
        mock_execute = Mock()

        mock_execute.data = []  # Empty data indicates failure
        mock_insert.execute.return_value = mock_execute
        mock_table.insert.return_value = mock_insert
        mock_supabase_client.table.return_value = mock_table

        # Test save should raise exception
        with pytest.raises(Exception, match="Failed to save haiku: no data returned"):
            repository.save(sample_haiku)

    def test_get_all_haikus(self, repository, mock_supabase_client):
        """Test getting all haikus."""
        # Mock response data
        mock_data = [
            {
                "id": "id1",
                "subject": "morning",
                "haiku_text": "Line 1\nLine 2\nLine 3",
                "created_at": "2024-01-15T10:30:00Z",
                "user_id": "user1",
            },
            {
                "id": "id2",
                "subject": "evening",
                "haiku_text": "Evening 1\nEvening 2\nEvening 3",
                "created_at": "2024-01-15T11:30:00Z",
                "user_id": "user2",
            },
        ]

        # Mock the Supabase response
        mock_table = Mock()
        mock_select = Mock()
        mock_order = Mock()
        mock_range = Mock()
        mock_execute = Mock()

        mock_execute.data = mock_data
        mock_range.execute.return_value = mock_execute
        mock_order.range.return_value = mock_range
        mock_select.order.return_value = mock_order
        mock_table.select.return_value = mock_select
        mock_supabase_client.table.return_value = mock_table

        # Test get_all
        result = repository.get_all(limit=10, offset=0)

        # Verify calls
        mock_supabase_client.table.assert_called_once_with("haikus")
        mock_table.select.assert_called_once_with("*")
        mock_select.order.assert_called_once_with("created_at", desc=True)
        mock_order.range.assert_called_once_with(0, 9)

        # Verify result
        assert len(result) == 2
        assert all(isinstance(haiku, Haiku) for haiku in result)
        assert result[0].subject == "morning"
        assert result[1].subject == "evening"

    def test_search_by_subject(self, repository, mock_supabase_client):
        """Test searching haikus by subject."""
        # Mock response data
        mock_data = [
            {
                "id": "id1",
                "subject": "coffee morning",
                "haiku_text": "Coffee haiku",
                "created_at": "2024-01-15T10:30:00Z",
                "user_id": "user1",
            }
        ]

        # Mock the Supabase response
        mock_table = Mock()
        mock_select = Mock()
        mock_ilike = Mock()
        mock_order = Mock()
        mock_limit = Mock()
        mock_execute = Mock()

        mock_execute.data = mock_data
        mock_limit.execute.return_value = mock_execute
        mock_order.limit.return_value = mock_limit
        mock_ilike.order.return_value = mock_order
        mock_select.ilike.return_value = mock_ilike
        mock_table.select.return_value = mock_select
        mock_supabase_client.table.return_value = mock_table

        # Test search
        result = repository.search_by_subject("coffee", limit=10)

        # Verify calls
        mock_supabase_client.table.assert_called_once_with("haikus")
        mock_table.select.assert_called_once_with("*")
        mock_select.ilike.assert_called_once_with("subject", "%coffee%")
        mock_ilike.order.assert_called_once_with("created_at", desc=True)
        mock_order.limit.assert_called_once_with(10)

        # Verify result
        assert len(result) == 1
        assert result[0].subject == "coffee morning"

    def test_get_by_id_found(self, repository, mock_supabase_client):
        """Test getting haiku by ID when found."""
        # Mock response data
        mock_data = [
            {
                "id": "test-id",
                "subject": "test subject",
                "haiku_text": "test haiku",
                "created_at": "2024-01-15T10:30:00Z",
                "user_id": "user1",
            }
        ]

        # Mock the Supabase response
        mock_table = Mock()
        mock_select = Mock()
        mock_eq = Mock()
        mock_execute = Mock()

        mock_execute.data = mock_data
        mock_eq.execute.return_value = mock_execute
        mock_select.eq.return_value = mock_eq
        mock_table.select.return_value = mock_select
        mock_supabase_client.table.return_value = mock_table

        # Test get_by_id
        result = repository.get_by_id("test-id")

        # Verify calls
        mock_supabase_client.table.assert_called_once_with("haikus")
        mock_table.select.assert_called_once_with("*")
        mock_select.eq.assert_called_once_with("id", "test-id")

        # Verify result
        assert isinstance(result, Haiku)
        assert result.id == "test-id"
        assert result.subject == "test subject"

    def test_get_by_id_not_found(self, repository, mock_supabase_client):
        """Test getting haiku by ID when not found."""
        # Mock empty response
        mock_table = Mock()
        mock_select = Mock()
        mock_eq = Mock()
        mock_execute = Mock()

        mock_execute.data = []
        mock_eq.execute.return_value = mock_execute
        mock_select.eq.return_value = mock_eq
        mock_table.select.return_value = mock_select
        mock_supabase_client.table.return_value = mock_table

        # Test get_by_id
        result = repository.get_by_id("nonexistent-id")

        # Verify result
        assert result is None

    def test_count_haikus(self, repository, mock_supabase_client):
        """Test counting haikus."""
        # Mock response
        mock_table = Mock()
        mock_select = Mock()
        mock_execute = Mock()

        mock_execute.count = 42
        mock_select.execute.return_value = mock_execute
        mock_table.select.return_value = mock_select
        mock_supabase_client.table.return_value = mock_table

        # Test count
        result = repository.count()

        # Verify calls
        mock_supabase_client.table.assert_called_once_with("haikus")
        mock_table.select.assert_called_once_with("id", count="exact")

        # Verify result
        assert result == 42

    def test_count_haikus_no_count(self, repository, mock_supabase_client):
        """Test counting haikus when count is None."""
        # Mock response with no count
        mock_table = Mock()
        mock_select = Mock()
        mock_execute = Mock()

        mock_execute.count = None
        mock_select.execute.return_value = mock_execute
        mock_table.select.return_value = mock_select
        mock_supabase_client.table.return_value = mock_table

        # Test count
        result = repository.count()

        # Verify result
        assert result == 0
