from app.domain.value_objects.document_status import DocumentStatus, can_transition_document_status


def test_valid_transitions() -> None:
    assert can_transition_document_status(DocumentStatus.UPLOADED, DocumentStatus.PROCESSING) is True
    assert can_transition_document_status(DocumentStatus.PROCESSING, DocumentStatus.PROCESSED) is True
    assert can_transition_document_status(DocumentStatus.PROCESSING, DocumentStatus.FAILED) is True
    assert can_transition_document_status(DocumentStatus.FAILED, DocumentStatus.PROCESSING) is True

def test_invalid_transitions() -> None:
    assert can_transition_document_status(DocumentStatus.UPLOADED, DocumentStatus.PROCESSED) is False
    assert can_transition_document_status(DocumentStatus.PROCESSED, DocumentStatus.UPLOADED) is False
    assert can_transition_document_status(DocumentStatus.FAILED, DocumentStatus.PROCESSED) is False
