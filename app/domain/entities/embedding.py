from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.exceptions.base import ValidationException


@dataclass
class Embedding:
    id: UUID
    vector: list[float]
    model: str
    dimension: int
    chunk_id: UUID | None
    question_id: UUID | None
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.vector:
            raise ValidationException("Embedding vector cannot be empty.")
        if self.dimension != len(self.vector):
            raise ValidationException(f"Dimension {self.dimension} does not match vector length {len(self.vector)}.")
        if not self.model or not self.model.strip():
            raise ValidationException("Model name cannot be empty.")
        if (self.chunk_id is None and self.question_id is None) or (self.chunk_id is not None and self.question_id is not None):
            raise ValidationException("Embedding must belong to either a chunk or a question, but not both.")

    @classmethod
    def create_for_chunk(
        cls,
        chunk_id: UUID,
        vector: list[float],
        model: str,
    ) -> "Embedding":
        return cls(
            id=uuid4(),
            vector=vector,
            model=model,
            dimension=len(vector),
            chunk_id=chunk_id,
            question_id=None,
            created_at=datetime.now(timezone.utc),
        )

    @classmethod
    def create_for_question(
        cls,
        question_id: UUID,
        vector: list[float],
        model: str,
    ) -> "Embedding":
        return cls(
            id=uuid4(),
            vector=vector,
            model=model,
            dimension=len(vector),
            chunk_id=None,
            question_id=question_id,
            created_at=datetime.now(timezone.utc),
        )
