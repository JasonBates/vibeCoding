"""Service layer for haiku storage operations."""
from __future__ import annotations

import logging
from typing import Any, List, Optional

try:  # pragma: no cover - exercised indirectly through repository tests
    from supabase import Client, create_client
except ModuleNotFoundError:  # pragma: no cover - executed in test environments
    Client = Any  # type: ignore

    def create_client(*_args: object, **_kwargs: object) -> "Client":  # type: ignore
        """Fallback client creator that surfaces missing dependency clearly."""
        raise RuntimeError(
            "Supabase dependency is not installed. Install 'supabase' to enable storage."
        )

from models import Haiku
from repository import HaikuRepository

logger = logging.getLogger(__name__)


class HaikuStorageService:
    """Service layer for haiku storage operations with business logic."""

    def __init__(self, supabase_url: str, supabase_key: str) -> None:
        """Initialize the service with Supabase credentials.

        Args:
            supabase_url: Supabase project URL
            supabase_key: Supabase anon/public API key
        """
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self._client: Optional[Client] = None
        self._repository: Optional[HaikuRepository] = None

    @property
    def client(self) -> Client:
        """Get or create Supabase client."""
        if self._client is None:
            try:
                self._client = create_client(self.supabase_url, self.supabase_key)
                logger.info("Supabase client created successfully")
            except Exception as e:
                logger.error("Failed to create Supabase client: %s", e)
                raise
        return self._client

    @property
    def repository(self) -> HaikuRepository:
        """Get or create repository instance."""
        if self._repository is None:
            self._repository = HaikuRepository(self.client)
        return self._repository

    def save_haiku(
        self, subject: str, haiku_text: str, user_id: Optional[str] = None
    ) -> Optional[Haiku]:
        """Save a haiku with validation and error handling.

        Args:
            subject: The subject of the haiku
            haiku_text: The generated haiku text
            user_id: Optional user ID for future authentication

        Returns:
            Saved Haiku instance if successful, None if failed
        """
        try:
            # Validate inputs
            if not subject or not subject.strip():
                logger.warning("Cannot save haiku: empty subject")
                return None

            if not haiku_text or not haiku_text.strip():
                logger.warning("Cannot save haiku: empty haiku text")
                return None

            # Create haiku instance
            haiku = Haiku(
                subject=subject.strip(), haiku_text=haiku_text.strip(), user_id=user_id
            )

            # Save to database
            saved_haiku = self.repository.save(haiku)
            logger.info("Successfully saved haiku: %s", saved_haiku.id)
            return saved_haiku

        except Exception as e:
            logger.error("Failed to save haiku: %s", e)
            return None

    def get_recent_haikus(self, limit: int = 10) -> List[Haiku]:
        """Get recent haikus with error handling.

        Args:
            limit: Maximum number of haikus to return

        Returns:
            List of recent Haiku instances (empty list if error)
        """
        try:
            return self.repository.get_all(limit=limit)
        except Exception as e:
            logger.error("Failed to get recent haikus: %s", e)
            return []

    def search_haikus(self, subject: str, limit: int = 10) -> List[Haiku]:
        """Search haikus by subject with error handling.

        Args:
            subject: Subject to search for
            limit: Maximum number of haikus to return

        Returns:
            List of matching Haiku instances (empty list if error)
        """
        try:
            if not subject or not subject.strip():
                return self.get_recent_haikus(limit)

            return self.repository.search_by_subject(subject.strip(), limit)
        except Exception as e:
            logger.error("Failed to search haikus: %s", e)
            return []

    def get_haiku_by_id(self, haiku_id: str) -> Optional[Haiku]:
        """Get a specific haiku by ID with error handling.

        Args:
            haiku_id: The ID of the haiku to retrieve

        Returns:
            Haiku instance if found, None if not found or error
        """
        try:
            return self.repository.get_by_id(haiku_id)
        except Exception as e:
            logger.error("Failed to get haiku by ID '%s': %s", haiku_id, e)
            return None

    def get_total_count(self) -> int:
        """Get total count of haikus with error handling.

        Returns:
            Total number of haikus (0 if error)
        """
        try:
            return self.repository.count()
        except Exception as e:
            logger.error("Failed to get haiku count: %s", e)
            return 0

    def is_available(self) -> bool:
        """Check if the storage service is available.

        Returns:
            True if service can connect to Supabase, False otherwise
        """
        try:
            # Try to get count as a simple connectivity test
            self.repository.count()
            return True
        except Exception as e:
            logger.warning("Storage service not available: %s", e)
            return False
