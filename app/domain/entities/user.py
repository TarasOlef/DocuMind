from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.exceptions.base import ValidationException
from app.domain.value_objects.permissions import Permission, has_permission
from app.domain.value_objects.roles import Role


@dataclass
class User:
    id: UUID
    email: str
    hashed_password: str
    role: Role
    organization_id: UUID | None
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.email or not self.email.strip():
            raise ValidationException("Email cannot be empty.")
        if not self.hashed_password:
            raise ValidationException("Hashed password cannot be empty.")

        # Normalize email
        self.email = self.email.strip().lower()

    @classmethod
    def create(
        cls,
        email: str,
        hashed_password: str,
        organization_id: UUID | None = None,
        role: Role = Role.USER,
    ) -> "User":
        return cls(
            id=uuid4(),
            email=email,
            hashed_password=hashed_password,
            role=role,
            organization_id=organization_id,
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)

    def activate(self) -> None:
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)

    def has_permission(self, permission: Permission) -> bool:
        return has_permission(self.role, permission)
