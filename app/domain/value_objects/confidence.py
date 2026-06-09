from dataclasses import dataclass

from app.domain.exceptions.base import ValidationException


@dataclass(frozen=True)
class ConfidenceScore:
    value: float

    def __post_init__(self) -> None:
        if not (0.0 <= self.value <= 1.0):
            raise ValidationException("Confidence score must be between 0.0 and 1.0")
