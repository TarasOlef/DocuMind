from app.domain.exceptions.base import DomainException


class UserAlreadyExistsException(DomainException):
    ...

class UserNotFoundException(DomainException):
    ...

class InactiveUserException(DomainException):
    ...
