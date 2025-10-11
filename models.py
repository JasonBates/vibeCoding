"""Data models for the haiku storage system."""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class Haiku:
    """Represents a haiku with metadata for storage."""

    subject: str
    haiku_text: str
    id: Optional[str] = None
    created_at: Optional[datetime] = None
    user_id: Optional[str] = None

    def __post_init__(self) -> None:
        """Set default values after initialization."""
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.utcnow()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Haiku:
        """Create a Haiku instance from a dictionary (e.g., from Supabase)."""
        return cls(
            id=data.get("id"),
            subject=data["subject"],
            haiku_text=data["haiku_text"],
            created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))
            if data.get("created_at")
            else None,
            user_id=data.get("user_id"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the Haiku instance to a dictionary for Supabase storage."""
        return {
            "id": self.id,
            "subject": self.subject,
            "haiku_text": self.haiku_text,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user_id": self.user_id,
        }

    def __str__(self) -> str:
        """String representation for display."""
        return (
            f"Haiku(id={self.id}, subject='{self.subject}', "
            f"created_at={self.created_at})"
        )
