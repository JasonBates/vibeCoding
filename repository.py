"""Repository layer for haiku data access using Supabase."""
from __future__ import annotations

import logging
from typing import List, Optional

from supabase import Client

from models import Haiku

logger = logging.getLogger(__name__)


class HaikuRepository:
    """Repository for haiku data operations using Supabase."""

    def __init__(self, supabase_client: Client) -> None:
        """Initialize repository with Supabase client.

        Args:
            supabase_client: Configured Supabase client instance
        """
        self.client = supabase_client
        self.table_name = "haikus"

    def save(self, haiku: Haiku) -> Haiku:
        """Save a haiku to the database.

        Args:
            haiku: Haiku instance to save

        Returns:
            The saved haiku with database-generated fields populated

        Raises:
            Exception: If database operation fails
        """
        try:
            data = haiku.to_dict()
            # Remove None values to avoid issues with Supabase
            data = {k: v for k, v in data.items() if v is not None}

            result = self.client.table(self.table_name).insert(data).execute()

            if not result.data:
                raise Exception("Failed to save haiku: no data returned")

            saved_data = result.data[0]
            return Haiku.from_dict(saved_data)

        except Exception as e:
            logger.error("Failed to save haiku: %s", e)
            raise

    def get_all(self, limit: int = 10, offset: int = 0) -> List[Haiku]:
        """Get all haikus ordered by creation date (newest first).

        Args:
            limit: Maximum number of haikus to return
            offset: Number of haikus to skip (for pagination)

        Returns:
            List of Haiku instances

        Raises:
            Exception: If database operation fails
        """
        try:
            result = (
                self.client.table(self.table_name)
                .select("*")
                .order("created_at", desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )

            return [Haiku.from_dict(row) for row in result.data]

        except Exception as e:
            logger.error("Failed to get haikus: %s", e)
            raise

    def search_by_subject(self, subject: str, limit: int = 10) -> List[Haiku]:
        """Search haikus by subject (case-insensitive partial match).

        Args:
            subject: Subject to search for
            limit: Maximum number of haikus to return

        Returns:
            List of matching Haiku instances

        Raises:
            Exception: If database operation fails
        """
        try:
            result = (
                self.client.table(self.table_name)
                .select("*")
                .ilike("subject", f"%{subject}%")
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )

            return [Haiku.from_dict(row) for row in result.data]

        except Exception as e:
            logger.error("Failed to search haikus by subject '%s': %s", subject, e)
            raise

    def get_by_id(self, haiku_id: str) -> Optional[Haiku]:
        """Get a specific haiku by its ID.

        Args:
            haiku_id: The ID of the haiku to retrieve

        Returns:
            Haiku instance if found, None otherwise

        Raises:
            Exception: If database operation fails
        """
        try:
            result = self.client.table(self.table_name).select("*").eq("id", haiku_id).execute()

            if not result.data:
                return None

            return Haiku.from_dict(result.data[0])

        except Exception as e:
            logger.error("Failed to get haiku by ID '%s': %s", haiku_id, e)
            raise

    def count(self) -> int:
        """Get the total count of haikus in the database.

        Returns:
            Total number of haikus

        Raises:
            Exception: If database operation fails
        """
        try:
            result = self.client.table(self.table_name).select("id", count="exact").execute()
            return result.count or 0

        except Exception as e:
            logger.error("Failed to count haikus: %s", e)
            raise

    def delete(self, haiku_id: str) -> bool:
        """Delete a haiku by its ID.

        Args:
            haiku_id: ID of the haiku to delete

        Returns:
            True if a haiku was deleted, False otherwise

        Raises:
            Exception: If database operation fails
        """
        try:
            result = self.client.table(self.table_name).delete().eq("id", haiku_id).execute()
            return bool(result.data)
        except Exception as e:
            logger.error("Failed to delete haiku '%s': %s", haiku_id, e)
            raise
