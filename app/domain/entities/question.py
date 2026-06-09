from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.exceptions.base import ValidationException


@dataclass
class Question:
    id: UUID
    user_id: UUID
    organization_id: UUID | None
    text: str
    document_ids: list[UUID]
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.text or not self.text.strip():
            raise ValidationException("Question text cannot be empty.")
        self.text = " ".join(self.text.split())

    @classmethod
    def create(
        cls,
        user_id: UUID,
        organization_id: UUID | None,
        text: str,
        document_ids: list[UUID] | None = None,
    ) -> "Question":
        return cls(
            id=uuid4(),
            user_id=user_id,
            organization_id=organization_id,
            text=text,
            document_ids=document_ids or [],
            created_at=datetime.now(timezone.utc),
        )

    def has_document_filter(self) -> bool:
        return len(self.document_ids) > 0
