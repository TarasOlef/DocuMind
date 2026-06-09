class DomainException(Exception):
    """Base exception for domain errors."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class ValidationException(DomainException):
    """Base exception for domain validation errors."""
