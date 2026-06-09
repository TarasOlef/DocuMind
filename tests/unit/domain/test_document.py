from uuid import uuid4

import pytest

from app.domain.entities.document import Document
from app.domain.entities.user import User
from app.domain.exceptions.base import ValidationException
from app.domain.exceptions.document_exceptions import InvalidDocumentStatusTransitionException
from app.domain.value_objects.document_status import DocumentStatus
from app.domain.value_objects.file_type import FileType
from app.domain.value_objects.roles import Role


def test_create_valid_document() -> None:
    owner_id = uuid4()
    doc = Document.create_uploaded(
        owner_id=owner_id,
        organization_id=None,
        filename="report.pdf",
        storage_path="/path/to/report.pdf"
    )
    assert doc.filename == "report.pdf"
    assert doc.file_type == FileType.PDF
    assert doc.status == DocumentStatus.UPLOADED
    assert doc.owner_id == owner_id

def test_document_empty_filename_raises_exception() -> None:
    with pytest.raises(ValidationException, match="Filename cannot be empty."):
        Document.create_uploaded(
            owner_id=uuid4(),
            organization_id=None,
            filename="   ",
            storage_path="/path/to/report.pdf"
        )

def test_document_empty_storage_path_raises_exception() -> None:
    with pytest.raises(ValidationException, match="Storage path cannot be empty."):
        Document.create_uploaded(
            owner_id=uuid4(),
            organization_id=None,
            filename="report.pdf",
            storage_path="   "
        )

def test_document_status_transitions() -> None:
    doc = Document.create_uploaded(
        owner_id=uuid4(),
        organization_id=None,
        filename="report.pdf",
        storage_path="/path"
    )
    assert doc.status == DocumentStatus.UPLOADED

    doc.mark_processing()
    assert doc.status == DocumentStatus.PROCESSING
    assert doc.updated_at is not None

    doc.mark_processed()
    assert doc.status == DocumentStatus.PROCESSED
    assert doc.processed_at is not None
    assert doc.failure_reason is None

def test_document_invalid_status_transition_raises_exception() -> None:
    doc = Document.create_uploaded(
        owner_id=uuid4(),
        organization_id=None,
        filename="report.pdf",
        storage_path="/path"
    )
    with pytest.raises(InvalidDocumentStatusTransitionException):
        doc.mark_processed() # Cannot go directly from UPLOADED to PROCESSED

def test_document_mark_failed() -> None:
    doc = Document.create_uploaded(
        owner_id=uuid4(),
        organization_id=None,
        filename="report.pdf",
        storage_path="/path"
    )
    doc.mark_processing()
    doc.mark_failed("Corrupted file")
    assert doc.status == DocumentStatus.FAILED
    assert doc.failure_reason == "Corrupted file"

def test_document_access_permissions() -> None:
    org_id = uuid4()
    owner_id = uuid4()
    other_user_id = uuid4()
    other_org_id = uuid4()

    doc = Document.create_uploaded(
        owner_id=owner_id,
        organization_id=org_id,
        filename="report.pdf",
        storage_path="/path"
    )

    owner = User.create(email="o@e.com", hashed_password="h", organization_id=org_id)
    owner.id = owner_id

    admin = User.create(email="a@e.com", hashed_password="h", role=Role.ADMIN)

    same_org_user = User.create(email="s@e.com", hashed_password="h", organization_id=org_id)
    same_org_user.id = other_user_id

    other_org_user = User.create(email="ex@e.com", hashed_password="h", organization_id=other_org_id)
    other_org_user.id = uuid4()

    assert doc.can_be_accessed_by(owner) is True
    assert doc.can_be_accessed_by(admin) is True
    assert doc.can_be_accessed_by(same_org_user) is True
    assert doc.can_be_accessed_by(other_org_user) is False
