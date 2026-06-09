from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.exceptions.base import ValidationException
from app.domain.value_objects.audit_action import AuditAction
from app.domain.value_objects.metadata import AuditMetadata

_FORBIDDEN_METADATA_KEYS = {"password", "token", "secret", "api_key", "authorization"}

@dataclass
class AuditLog:
    id: UUID
    user_id: UUID | None
    organization_id: UUID | None
    action: AuditAction
    resource_type: str | None
    resource_id: UUID | None
    metadata: AuditMetadata
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.action:
            raise ValidationException("Audit action is mandatory.")

        # Check for forbidden keys in metadata
        if self.metadata:
            for key in self.metadata.keys():
                if any(forbidden in key.lower() for forbidden in _FORBIDDEN_METADATA_KEYS):
                    raise ValidationException(f"Audit log metadata contains forbidden key: {key}")

    @classmethod
    def create(
        cls,
        action: AuditAction,
        user_id: UUID | None = None,
        organization_id: UUID | None = None,
        resource_type: str | None = None,
        resource_id: UUID | None = None,
        metadata: AuditMetadata | None = None,
    ) -> "AuditLog":
        return cls(
            id=uuid4(),
            user_id=user_id,
            organization_id=organization_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            metadata=metadata or {},
            created_at=datetime.now(timezone.utc),
        )
