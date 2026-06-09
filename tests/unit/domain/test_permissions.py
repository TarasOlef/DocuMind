from app.domain.value_objects.permissions import Permission, has_permission
from app.domain.value_objects.roles import Role


def test_user_permissions_are_correct() -> None:
    assert has_permission(Role.USER, Permission.ASK_QUESTIONS) is True
    assert has_permission(Role.USER, Permission.VIEW_AUDIT_LOGS) is False

def test_admin_permissions_are_correct() -> None:
    assert has_permission(Role.ADMIN, Permission.ASK_QUESTIONS) is True
    assert has_permission(Role.ADMIN, Permission.VIEW_AUDIT_LOGS) is True
    assert has_permission(Role.ADMIN, Permission.MANAGE_ORGANIZATION) is True
