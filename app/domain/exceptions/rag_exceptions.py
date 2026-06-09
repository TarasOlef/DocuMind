from app.domain.exceptions.base import DomainException


class EmbeddingGenerationException(DomainException):
    ...

class NoRelevantContextFoundException(DomainException):
    ...

class LLMProviderException(DomainException):
    ...

class AnswerValidationException(DomainException):
    ...
