from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.exceptions.base import ValidationException


@dataclass
class Organization:
    id: UUID
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationException("Organization name cannot be empty.")
        self.name = self.name.strip()

    @classmethod
    def create(cls, name: str) -> "Organization":
        return cls(
            id=uuid4(),
            name=name,
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )

    def rename(self, new_name: str) -> None:
        if not new_name or not new_name.strip():
            raise ValidationException("New organization name cannot be empty.")
        self.name = new_name.strip()
        self.updated_at = datetime.now(timezone.utc)

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)
