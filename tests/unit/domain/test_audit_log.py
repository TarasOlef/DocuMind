from uuid import uuid4

import pytest

from app.domain.entities.audit_log import AuditLog
from app.domain.exceptions.base import ValidationException
from app.domain.value_objects.audit_action import AuditAction


def test_create_valid_audit_log() -> None:
    log = AuditLog.create(
        action=AuditAction.USER_LOGGED_IN,
        user_id=uuid4()
    )
    assert log.action == AuditAction.USER_LOGGED_IN

def test_audit_log_forbidden_metadata() -> None:
    forbidden_keys = ["password", "token", "secret", "api_key", "authorization", "my_PASSWORD_field"]
    for key in forbidden_keys:
        with pytest.raises(ValidationException, match="Audit log metadata contains forbidden key"):
            AuditLog.create(
                action=AuditAction.USER_LOGGED_IN,
                metadata={key: "value"}
            )

def test_audit_log_valid_metadata() -> None:
    log = AuditLog.create(
        action=AuditAction.USER_LOGGED_IN,
        metadata={"ip_address": "127.0.0.1", "browser": "chrome"}
    )
    assert log.metadata["ip_address"] == "127.0.0.1"
