from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.exceptions.base import ValidationException


@dataclass
class Citation:
    id: UUID
    answer_id: UUID
    document_id: UUID
    chunk_id: UUID
    document_name: str
    page_number: int | None
    excerpt: str
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.document_name or not self.document_name.strip():
            raise ValidationException("Document name cannot be empty.")
        if not self.excerpt or not self.excerpt.strip():
            raise ValidationException("Excerpt cannot be empty.")
        if self.page_number is not None and self.page_number <= 0:
            raise ValidationException("Page number must be greater than 0.")

    @classmethod
    def create(
        cls,
        answer_id: UUID,
        document_id: UUID,
        chunk_id: UUID,
        document_name: str,
        excerpt: str,
        page_number: int | None = None,
    ) -> "Citation":
        return cls(
            id=uuid4(),
            answer_id=answer_id,
            document_id=document_id,
            chunk_id=chunk_id,
            document_name=document_name.strip(),
            page_number=page_number,
            excerpt=excerpt.strip(),
            created_at=datetime.now(timezone.utc),
        )
