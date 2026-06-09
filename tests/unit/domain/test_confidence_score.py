import pytest

from app.domain.exceptions.base import ValidationException
from app.domain.value_objects.confidence import ConfidenceScore


def test_confidence_score_valid() -> None:
    assert ConfidenceScore(0.0).value == 0.0
    assert ConfidenceScore(1.0).value == 1.0
    assert ConfidenceScore(0.5).value == 0.5

def test_confidence_score_invalid() -> None:
    with pytest.raises(ValidationException, match="Confidence score must be between 0.0 and 1.0"):
        ConfidenceScore(-0.1)

    with pytest.raises(ValidationException, match="Confidence score must be between 0.0 and 1.0"):
        ConfidenceScore(1.1)
