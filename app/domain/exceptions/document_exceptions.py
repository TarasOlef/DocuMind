from app.domain.exceptions.base import DomainException


class DocumentNotFoundException(DomainException):
    ...

class UnauthorizedDocumentAccessException(DomainException):
    ...

class DocumentProcessingException(DomainException):
    ...

class InvalidFileTypeException(DomainException):
    ...

class InvalidDocumentStatusTransitionException(DomainException):
    ...
