class ApplicationError(Exception):
    """
    Base class for all application specific errors.
    Allows catching any domain/application error cleanly at the API layer.
    """
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
