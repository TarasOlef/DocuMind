from app.domain.exceptions.base import DomainException


class PermissionDeniedException(DomainException):
    ...

class InvalidRoleException(DomainException):
    ...
