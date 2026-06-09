import pytest

from app.domain.entities.user import User
from app.domain.exceptions.base import ValidationException
from app.domain.value_objects.permissions import Permission
from app.domain.value_objects.roles import Role


def test_create_valid_user() -> None:
    user = User.create(
        email=" Test@Example.com ",
        hashed_password="hashed_secret"
    )
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed_secret"
    assert user.role == Role.USER
    assert user.is_active is True
    assert user.created_at is not None

def test_user_empty_email_raises_exception() -> None:
    with pytest.raises(ValidationException, match="Email cannot be empty."):
        User.create(email="   ", hashed_password="hashed_secret")

def test_user_empty_password_raises_exception() -> None:
    with pytest.raises(ValidationException, match="Hashed password cannot be empty."):
        User.create(email="test@example.com", hashed_password="")

def test_user_permissions() -> None:
    user = User.create(email="test@example.com", hashed_password="hash")
    admin = User.create(email="admin@example.com", hashed_password="hash", role=Role.ADMIN)

    assert user.has_permission(Permission.ASK_QUESTIONS) is True
    assert user.has_permission(Permission.VIEW_AUDIT_LOGS) is False

    assert admin.has_permission(Permission.ASK_QUESTIONS) is True
    assert admin.has_permission(Permission.VIEW_AUDIT_LOGS) is True

def test_user_deactivate_and_activate() -> None:
    user = User.create(email="test@example.com", hashed_password="hash")
    assert user.is_active is True

    user.deactivate()
    assert user.is_active is False
    assert user.updated_at is not None

    user.activate()
    assert user.is_active is True
