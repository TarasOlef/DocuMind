from enum import Enum


class DocumentStatus(str, Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"

def can_transition_document_status(
    current: DocumentStatus,
    target: DocumentStatus,
) -> bool:
    """Check if a transition from current status to target status is valid."""
    valid_transitions = {
        DocumentStatus.UPLOADED: {DocumentStatus.PROCESSING},
        DocumentStatus.PROCESSING: {DocumentStatus.PROCESSED, DocumentStatus.FAILED},
        DocumentStatus.FAILED: {DocumentStatus.PROCESSING},  # allow retry
        DocumentStatus.PROCESSED: set(),  # terminal state
    }

    return target in valid_transitions.get(current, set())
