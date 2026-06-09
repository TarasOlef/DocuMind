from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.exceptions.base import ValidationException
from app.domain.value_objects.confidence import ConfidenceScore


@dataclass
class Answer:
    id: UUID
    question_id: UUID
    text: str
    confidence: ConfidenceScore
    reasoning_summary: str
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.text or not self.text.strip():
            raise ValidationException("Answer text cannot be empty.")
        if not self.reasoning_summary or not self.reasoning_summary.strip():
            raise ValidationException("Reasoning summary cannot be empty.")

    @classmethod
    def create(
        cls,
        question_id: UUID,
        text: str,
        confidence_value: float,
        reasoning_summary: str,
    ) -> "Answer":
        return cls(
            id=uuid4(),
            question_id=question_id,
            text=text,
            confidence=ConfidenceScore(value=confidence_value),
            reasoning_summary=reasoning_summary,
            created_at=datetime.now(timezone.utc),
        )

    def is_low_confidence(self) -> bool:
        return self.confidence.value < 0.5
