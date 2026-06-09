from enum import Enum

from app.domain.value_objects.roles import Role


class Permission(str, Enum):
    READ_OWN_DOCUMENTS = "READ_OWN_DOCUMENTS"
    UPLOAD_DOCUMENTS = "UPLOAD_DOCUMENTS"
    PROCESS_OWN_DOCUMENTS = "PROCESS_OWN_DOCUMENTS"
    ASK_QUESTIONS = "ASK_QUESTIONS"
    VIEW_OWN_HISTORY = "VIEW_OWN_HISTORY"
    VIEW_AUDIT_LOGS = "VIEW_AUDIT_LOGS"
    MANAGE_ORGANIZATION = "MANAGE_ORGANIZATION"

ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.USER: {
        Permission.READ_OWN_DOCUMENTS,
        Permission.UPLOAD_DOCUMENTS,
        Permission.PROCESS_OWN_DOCUMENTS,
        Permission.ASK_QUESTIONS,
        Permission.VIEW_OWN_HISTORY,
    },
    Role.ADMIN: {
        Permission.READ_OWN_DOCUMENTS,
        Permission.UPLOAD_DOCUMENTS,
        Permission.PROCESS_OWN_DOCUMENTS,
        Permission.ASK_QUESTIONS,
        Permission.VIEW_OWN_HISTORY,
        Permission.VIEW_AUDIT_LOGS,
        Permission.MANAGE_ORGANIZATION,
    },
}

def has_permission(role: Role, permission: Permission) -> bool:
    """Check if a specific role has a given permission."""
    return permission in ROLE_PERMISSIONS.get(role, set())
