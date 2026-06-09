from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.entities.user import User
from app.domain.exceptions.base import ValidationException
from app.domain.exceptions.document_exceptions import InvalidDocumentStatusTransitionException
from app.domain.value_objects.document_status import DocumentStatus, can_transition_document_status
from app.domain.value_objects.file_type import FileType, file_type_from_filename
from app.domain.value_objects.metadata import DocumentMetadata
from app.domain.value_objects.roles import Role


@dataclass
class Document:
    id: UUID
    owner_id: UUID
    organization_id: UUID | None
    filename: str
    file_type: FileType
    storage_path: str
    status: DocumentStatus
    metadata: DocumentMetadata
    created_at: datetime
    updated_at: datetime | None = None
    processed_at: datetime | None = None
    failure_reason: str | None = None

    def __post_init__(self) -> None:
        if not self.filename or not self.filename.strip():
            raise ValidationException("Filename cannot be empty.")
        if not self.storage_path or not self.storage_path.strip():
            raise ValidationException("Storage path cannot be empty.")

    @classmethod
    def create_uploaded(
        cls,
        owner_id: UUID,
        organization_id: UUID | None,
        filename: str,
        storage_path: str,
        metadata: DocumentMetadata | None = None,
    ) -> "Document":
        if not filename or not filename.strip():
            raise ValidationException("Filename cannot be empty.")

        file_type = file_type_from_filename(filename)
        return cls(
            id=uuid4(),
            owner_id=owner_id,
            organization_id=organization_id,
            filename=filename.strip(),
            file_type=file_type,
            storage_path=storage_path,
            status=DocumentStatus.UPLOADED,
            metadata=metadata or {},
            created_at=datetime.now(timezone.utc),
        )

    def _transition_to(self, new_status: DocumentStatus) -> None:
        if not can_transition_document_status(self.status, new_status):
            raise InvalidDocumentStatusTransitionException(
                f"Cannot transition document from {self.status.value} to {new_status.value}"
            )
        self.status = new_status
        self.updated_at = datetime.now(timezone.utc)

    def mark_processing(self) -> None:
        self._transition_to(DocumentStatus.PROCESSING)

    def mark_processed(self) -> None:
        self._transition_to(DocumentStatus.PROCESSED)
        self.processed_at = datetime.now(timezone.utc)
        self.failure_reason = None

    def mark_failed(self, reason: str) -> None:
        self._transition_to(DocumentStatus.FAILED)
        self.failure_reason = reason

    def can_be_accessed_by(self, user: User) -> bool:
        if user.role == Role.ADMIN:
            return True
        if self.belongs_to_user(user.id):
            return True
        if self.organization_id and self.organization_id == user.organization_id:
            return True
        return False

    def belongs_to_user(self, user_id: UUID) -> bool:
        return self.owner_id == user_id
