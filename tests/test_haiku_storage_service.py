"""Tests for the haiku storage service layer."""
from __future__ import annotations

from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from haiku_storage_service import HaikuStorageService
from models import Haiku


class TestHaikuStorageService:
    """Test cases for HaikuStorageService."""

    @pytest.fixture
    def mock_repository(self):
        """Mock repository for testing."""
        return Mock()

    @pytest.fixture
    def service(self, mock_repository):
        """Create service instance with mocked repository."""
        with patch("haiku_storage_service.HaikuRepository") as mock_repo_class:
            mock_repo_class.return_value = mock_repository
            service = HaikuStorageService("http://test.supabase.co", "test-key")
            service._repository = mock_repository
            return service

    @pytest.fixture
    def sample_haiku(self):
        """Sample poem for testing."""
        return Haiku(
            subject="coffee morning",
            haiku_text=(
                "Silent mind explored in hush of dawn. Dreams wander through lavender air. We breathe the promise of morning.\n\n"
                "Moonlight drifts across the quiet lake. Memories ripple in silver whispers. We hold the night between our hands."
            ),
            id="test-id-123",
            created_at=datetime(2024, 1, 15, 10, 30, 0),
            user_id="user-123",
        )

    def test_save_haiku_success(self, service, mock_repository, sample_haiku):
        """Test successful haiku saving."""
        # Mock repository response
        mock_repository.save.return_value = sample_haiku

        # Test save
        result = service.save_haiku("coffee morning", "test poem text")

        # Verify calls
        mock_repository.save.assert_called_once()
        saved_haiku = mock_repository.save.call_args[0][0]
        assert saved_haiku.subject == "coffee morning"
        assert saved_haiku.haiku_text == "test poem text"

        # Verify result
        assert result == sample_haiku

    def test_save_haiku_empty_subject(self, service, mock_repository):
        """Test saving haiku with empty subject."""
        # Test save with empty subject
        result = service.save_haiku("", "test poem text")

        # Verify repository not called
        mock_repository.save.assert_not_called()

        # Verify result
        assert result is None

    def test_save_haiku_empty_text(self, service, mock_repository):
        """Test saving haiku with empty text."""
        # Test save with empty text
        result = service.save_haiku("coffee morning", "")

        # Verify repository not called
        mock_repository.save.assert_not_called()

        # Verify result
        assert result is None

    def test_save_haiku_whitespace_only(self, service, mock_repository):
        """Test saving haiku with whitespace-only inputs."""
        # Test save with whitespace-only subject
        result = service.save_haiku("   ", "test poem text")
        assert result is None

        # Test save with whitespace-only text
        result = service.save_haiku("coffee morning", "   ")
        assert result is None

        # Verify repository not called
        mock_repository.save.assert_not_called()

    def test_save_haiku_repository_error(self, service, mock_repository):
        """Test saving haiku when repository raises exception."""
        # Mock repository to raise exception
        mock_repository.save.side_effect = Exception("Database error")

        # Test save
        result = service.save_haiku("coffee morning", "test poem text")

        # Verify result
        assert result is None

    def test_get_recent_haikus_success(self, service, mock_repository, sample_haiku):
        """Test getting recent haikus successfully."""
        # Mock repository response
        mock_repository.get_all.return_value = [sample_haiku]

        # Test get_recent_haikus
        result = service.get_recent_haikus(limit=5)

        # Verify calls
        mock_repository.get_all.assert_called_once_with(limit=5)

        # Verify result
        assert result == [sample_haiku]

    def test_get_recent_haikus_repository_error(self, service, mock_repository):
        """Test getting recent haikus when repository raises exception."""
        # Mock repository to raise exception
        mock_repository.get_all.side_effect = Exception("Database error")

        # Test get_recent_haikus
        result = service.get_recent_haikus(limit=5)

        # Verify result
        assert result == []

    def test_search_haikus_with_query(self, service, mock_repository, sample_haiku):
        """Test searching haikus with a query."""
        # Mock repository response
        mock_repository.search_by_subject.return_value = [sample_haiku]

        # Test search
        result = service.search_haikus("coffee", limit=5)

        # Verify calls
        mock_repository.search_by_subject.assert_called_once_with("coffee", 5)

        # Verify result
        assert result == [sample_haiku]

    def test_search_haikus_empty_query(self, service, mock_repository, sample_haiku):
        """Test searching haikus with empty query falls back to recent."""
        # Mock repository response
        mock_repository.get_all.return_value = [sample_haiku]

        # Test search with empty query
        result = service.search_haikus("", limit=5)

        # Verify calls
        mock_repository.get_all.assert_called_once_with(limit=5)
        mock_repository.search_by_subject.assert_not_called()

        # Verify result
        assert result == [sample_haiku]

    def test_search_haikus_whitespace_query(
        self, service, mock_repository, sample_haiku
    ):
        """Test searching haikus with whitespace-only query falls back to recent."""
        # Mock repository response
        mock_repository.get_all.return_value = [sample_haiku]

        # Test search with whitespace-only query
        result = service.search_haikus("   ", limit=5)

        # Verify calls
        mock_repository.get_all.assert_called_once_with(limit=5)
        mock_repository.search_by_subject.assert_not_called()

        # Verify result
        assert result == [sample_haiku]

    def test_search_haikus_repository_error(self, service, mock_repository):
        """Test searching haikus when repository raises exception."""
        # Mock repository to raise exception
        mock_repository.search_by_subject.side_effect = Exception("Database error")

        # Test search
        result = service.search_haikus("coffee", limit=5)

        # Verify result
        assert result == []

    def test_get_haiku_by_id_success(self, service, mock_repository, sample_haiku):
        """Test getting haiku by ID successfully."""
        # Mock repository response
        mock_repository.get_by_id.return_value = sample_haiku

        # Test get_haiku_by_id
        result = service.get_haiku_by_id("test-id")

        # Verify calls
        mock_repository.get_by_id.assert_called_once_with("test-id")

        # Verify result
        assert result == sample_haiku

    def test_get_haiku_by_id_not_found(self, service, mock_repository):
        """Test getting haiku by ID when not found."""
        # Mock repository response
        mock_repository.get_by_id.return_value = None

        # Test get_haiku_by_id
        result = service.get_haiku_by_id("nonexistent-id")

        # Verify result
        assert result is None

    def test_get_haiku_by_id_repository_error(self, service, mock_repository):
        """Test getting haiku by ID when repository raises exception."""
        # Mock repository to raise exception
        mock_repository.get_by_id.side_effect = Exception("Database error")

        # Test get_haiku_by_id
        result = service.get_haiku_by_id("test-id")

        # Verify result
        assert result is None

    def test_get_total_count_success(self, service, mock_repository):
        """Test getting total count successfully."""
        # Mock repository response
        mock_repository.count.return_value = 42

        # Test get_total_count
        result = service.get_total_count()

        # Verify calls
        mock_repository.count.assert_called_once()

        # Verify result
        assert result == 42

    def test_get_total_count_repository_error(self, service, mock_repository):
        """Test getting total count when repository raises exception."""
        # Mock repository to raise exception
        mock_repository.count.side_effect = Exception("Database error")

        # Test get_total_count
        result = service.get_total_count()

        # Verify result
        assert result == 0

    def test_is_available_true(self, service, mock_repository):
        """Test service availability when repository works."""
        # Mock repository to work
        mock_repository.count.return_value = 0

        # Test is_available
        result = service.is_available()

        # Verify result
        assert result is True

    def test_is_available_false(self, service, mock_repository):
        """Test service availability when repository fails."""
        # Mock repository to fail
        mock_repository.count.side_effect = Exception("Connection error")

        # Test is_available
        result = service.is_available()

        # Verify result
        assert result is False

    def test_client_property_creation(self):
        """Test Supabase client creation."""
        with patch("haiku_storage_service.create_client") as mock_create_client:
            mock_client = Mock()
            mock_create_client.return_value = mock_client

            service = HaikuStorageService("http://test.supabase.co", "test-key")
            client = service.client

            # Verify client creation
            mock_create_client.assert_called_once_with(
                "http://test.supabase.co", "test-key"
            )
            assert client == mock_client

    def test_client_property_caching(self):
        """Test that client is cached after first creation."""
        with patch("haiku_storage_service.create_client") as mock_create_client:
            mock_client = Mock()
            mock_create_client.return_value = mock_client

            service = HaikuStorageService("http://test.supabase.co", "test-key")

            # Call client property multiple times
            client1 = service.client
            client2 = service.client

            # Verify client created only once
            mock_create_client.assert_called_once()
            assert client1 == client2 == mock_client

    def test_repository_property_creation(self):
        """Test repository property creation."""
        # Create a fresh service without pre-set repository
        with patch("haiku_storage_service.create_client") as mock_create_client:
            mock_client = Mock()
            mock_create_client.return_value = mock_client

            service = HaikuStorageService("http://test.supabase.co", "test-key")

            with patch("haiku_storage_service.HaikuRepository") as mock_repo_class:
                mock_repository = Mock()
                mock_repo_class.return_value = mock_repository

                # Access repository property
                repo = service.repository

                # Verify repository creation
                mock_repo_class.assert_called_once_with(mock_client)
                assert repo == mock_repository

    def test_repository_property_caching(self):
        """Test that repository is cached after first creation."""
        # Create a fresh service without pre-set repository
        with patch("haiku_storage_service.create_client") as mock_create_client:
            mock_client = Mock()
            mock_create_client.return_value = mock_client

            service = HaikuStorageService("http://test.supabase.co", "test-key")

            with patch("haiku_storage_service.HaikuRepository") as mock_repo_class:
                mock_repository = Mock()
                mock_repo_class.return_value = mock_repository

                # Access repository property multiple times
                repo1 = service.repository
                repo2 = service.repository

                # Verify repository created only once
                mock_repo_class.assert_called_once()
                assert repo1 == repo2 == mock_repository
