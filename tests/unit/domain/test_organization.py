import pytest

from app.domain.entities.organization import Organization
from app.domain.exceptions.base import ValidationException


def test_create_valid_organization() -> None:
    org = Organization.create(name="  Acme Corp  ")
    assert org.name == "Acme Corp"
    assert org.is_active is True
    assert org.created_at is not None

def test_organization_empty_name_raises_exception() -> None:
    with pytest.raises(ValidationException, match="Organization name cannot be empty."):
        Organization.create(name="   ")

def test_organization_rename() -> None:
    org = Organization.create(name="Acme Corp")
    org.rename("  Acme Global  ")
    assert org.name == "Acme Global"
    assert org.updated_at is not None

def test_organization_deactivate() -> None:
    org = Organization.create(name="Acme Corp")
    assert org.is_active is True

    org.deactivate()
    assert org.is_active is False
    assert org.updated_at is not None
