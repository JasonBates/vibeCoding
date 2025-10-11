"""Integration tests for Supabase haiku storage."""
from __future__ import annotations

import os
from datetime import datetime
from typing import List

import pytest

from haiku_storage_service import HaikuStorageService
from models import Haiku


@pytest.mark.integration
class TestSupabaseIntegration:
    """Integration tests for Supabase haiku storage."""

    @pytest.fixture
    def storage_service(self):
        """Create storage service for integration tests."""
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        if not supabase_url or not supabase_key:
            pytest.fail(
                "Supabase credentials not configured - "
                "SUPABASE_URL and SUPABASE_KEY required"
            )

        # Create service and check if it's actually available
        service = HaikuStorageService(supabase_url, supabase_key)
        if not service.is_available():
            pytest.fail(
                "Supabase service not available - check your credentials and connection"
            )

        return service

    @pytest.fixture
    def test_haiku_ids(self):
        """Track haiku IDs created during tests for cleanup."""
        return []

    @pytest.fixture(autouse=True)
    def cleanup_test_data(self, storage_service, test_haiku_ids):
        """Automatically clean up test data after each test."""
        yield  # Run the test
        # Cleanup after test completes
        if test_haiku_ids and storage_service.is_available():
            try:
                for haiku_id in test_haiku_ids:
                    # Delete each test haiku by ID
                    storage_service.client.table("haikus").delete().eq(
                        "id", haiku_id
                    ).execute()
            except Exception as e:
                print(f"Warning: Failed to cleanup test data: {e}")

    def _create_test_haiku(
        self, storage_service, test_haiku_ids, subject_suffix="", text="Test haiku"
    ):
        """Helper method to create a test haiku and track it for cleanup."""
        test_subject = f"test-{datetime.now().timestamp()}{subject_suffix}"
        test_text = (
            text
            if text != "Test haiku"
            else "Test haiku line one\nTest haiku line two\nTest haiku line three"
        )

        saved_haiku = storage_service.save_haiku(test_subject, test_text)
        if saved_haiku:
            test_haiku_ids.append(saved_haiku.id)
        return saved_haiku

    def test_service_availability(self, storage_service):
        """Test that storage service can connect to Supabase."""
        assert storage_service.is_available()

    def test_save_and_retrieve_haiku(self, storage_service, test_haiku_ids):
        """Test saving a haiku and retrieving it."""
        # Create test haiku using helper method
        saved_haiku = self._create_test_haiku(storage_service, test_haiku_ids)

        # Verify save was successful
        assert saved_haiku is not None
        assert saved_haiku.subject.startswith("test-")
        assert (
            saved_haiku.haiku_text
            == "Test haiku line one\nTest haiku line two\nTest haiku line three"
        )
        assert saved_haiku.id is not None
        assert saved_haiku.created_at is not None

    def test_get_recent_haikus(self, storage_service, test_haiku_ids):
        """Test retrieving recent haikus."""
        # Save a test haiku first using helper method
        self._create_test_haiku(
            storage_service, test_haiku_ids, "-recent", "Recent test haiku"
        )

        # Get recent haikus
        recent_haikus = storage_service.get_recent_haikus(limit=5)

        # Verify we got some haikus
        assert isinstance(recent_haikus, list)
        assert len(recent_haikus) > 0

        # Verify all haikus are Haiku instances
        for haiku in recent_haikus:
            assert isinstance(haiku, Haiku)
            assert haiku.subject is not None
            assert haiku.haiku_text is not None
            assert haiku.id is not None
            assert haiku.created_at is not None

    def test_search_haikus_by_subject(self, storage_service, test_haiku_ids):
        """Test searching haikus by subject."""
        # Save a test haiku with unique subject using helper method
        saved_haiku = self._create_test_haiku(
            storage_service, test_haiku_ids, "-search", "Search test haiku"
        )
        unique_subject = saved_haiku.subject

        # Search for the haiku
        search_results = storage_service.search_haikus(unique_subject, limit=10)

        # Verify we found the haiku
        assert isinstance(search_results, list)
        assert len(search_results) > 0

        # Verify the haiku is in results
        found_haiku = None
        for haiku in search_results:
            if haiku.subject == unique_subject:
                found_haiku = haiku
                break

        assert found_haiku is not None
        assert found_haiku.haiku_text == "Search test haiku"

    def test_search_haikus_partial_match(self, storage_service, test_haiku_ids):
        """Test searching haikus with partial subject match."""
        # Save a test haiku with unique subject using helper method
        saved_haiku = self._create_test_haiku(
            storage_service, test_haiku_ids, "-partial", "Partial search test haiku"
        )
        unique_subject = saved_haiku.subject

        # Search with partial subject
        search_term = "partial"
        search_results = storage_service.search_haikus(search_term, limit=10)

        # Verify we found the haiku
        assert isinstance(search_results, list)
        assert len(search_results) > 0

        # Verify the haiku is in results
        found_haiku = None
        for haiku in search_results:
            if search_term.lower() in haiku.subject.lower():
                found_haiku = haiku
                break

        assert found_haiku is not None
        assert found_haiku.subject == unique_subject

    def test_get_haiku_by_id(self, storage_service, test_haiku_ids):
        """Test retrieving a specific haiku by ID."""
        # Save a test haiku first using helper method
        saved_haiku = self._create_test_haiku(
            storage_service, test_haiku_ids, "-id", "ID test haiku"
        )

        assert saved_haiku is not None
        haiku_id = saved_haiku.id

        # Retrieve haiku by ID
        retrieved_haiku = storage_service.get_haiku_by_id(haiku_id)

        # Verify retrieval
        assert retrieved_haiku is not None
        assert retrieved_haiku.id == haiku_id
        assert retrieved_haiku.subject == saved_haiku.subject
        assert retrieved_haiku.haiku_text == saved_haiku.haiku_text

    def test_get_nonexistent_haiku_by_id(self, storage_service, test_haiku_ids):
        """Test retrieving a haiku with non-existent ID."""
        # Try to get a haiku with a fake ID
        fake_id = "00000000-0000-0000-0000-000000000000"
        retrieved_haiku = storage_service.get_haiku_by_id(fake_id)

        # Should return None for non-existent haiku
        assert retrieved_haiku is None

    def test_get_total_count(self, storage_service, test_haiku_ids):
        """Test getting total count of haikus."""
        # Get initial count
        initial_count = storage_service.get_total_count()

        # Save a test haiku using helper method
        self._create_test_haiku(
            storage_service, test_haiku_ids, "-count", "Count test haiku"
        )

        # Get count after adding haiku
        new_count = storage_service.get_total_count()

        # Count should have increased by 1
        assert new_count == initial_count + 1

    def test_save_haiku_with_user_id(self, storage_service, test_haiku_ids):
        """Test saving haiku with user ID."""
        # Create test haiku with user ID using helper method
        test_subject = f"test-{datetime.now().timestamp()}-user"
        test_text = "User test haiku"
        user_id = "550e8400-e29b-41d4-a716-446655440000"

        # Save haiku
        saved_haiku = storage_service.save_haiku(test_subject, test_text, user_id)
        if saved_haiku:
            test_haiku_ids.append(saved_haiku.id)

        # Verify save was successful
        assert saved_haiku is not None
        assert saved_haiku.subject == test_subject
        assert saved_haiku.haiku_text == test_text
        assert saved_haiku.user_id == user_id

    def test_error_handling_invalid_credentials(self):
        """Test error handling with invalid Supabase credentials."""
        # Create service with invalid credentials
        invalid_service = HaikuStorageService("https://invalid.url", "invalid_key")

        # Should not be available
        assert not invalid_service.is_available()

    def test_haiku_ordering_by_created_at(self, storage_service, test_haiku_ids):
        """Test that haikus are ordered by created_at in descending order."""
        # Save multiple test haikus with slight delays using helper method
        import time

        saved_haiku1 = self._create_test_haiku(
            storage_service, test_haiku_ids, "-order1", "First haiku"
        )

        time.sleep(0.1)  # Small delay to ensure different timestamps

        saved_haiku2 = self._create_test_haiku(
            storage_service, test_haiku_ids, "-order2", "Second haiku"
        )

        # Get recent haikus
        recent_haikus = storage_service.get_recent_haikus(limit=10)

        # Verify ordering (most recent first)
        assert len(recent_haikus) >= 2

        # Check that timestamps are in descending order
        for i in range(len(recent_haikus) - 1):
            assert recent_haikus[i].created_at >= recent_haikus[i + 1].created_at
