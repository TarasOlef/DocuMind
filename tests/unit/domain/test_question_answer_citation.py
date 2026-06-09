from uuid import uuid4

import pytest

from app.domain.entities.answer import Answer
from app.domain.entities.citation import Citation
from app.domain.entities.question import Question
from app.domain.exceptions.base import ValidationException


def test_create_valid_question() -> None:
    q = Question.create(
        user_id=uuid4(),
        organization_id=None,
        text="  What is the capital of France?  "
    )
    assert q.text == "What is the capital of France?"
    assert q.has_document_filter() is False

def test_question_empty_text_raises_exception() -> None:
    with pytest.raises(ValidationException, match="Question text cannot be empty."):
        Question.create(user_id=uuid4(), organization_id=None, text="   ")

def test_create_valid_answer() -> None:
    a = Answer.create(
        question_id=uuid4(),
        text="Paris is the capital.",
        confidence_value=0.9,
        reasoning_summary="Found in doc 1"
    )
    assert a.text == "Paris is the capital."
    assert a.confidence.value == 0.9
    assert a.is_low_confidence() is False

def test_answer_empty_text_raises_exception() -> None:
    with pytest.raises(ValidationException, match="Answer text cannot be empty."):
        Answer.create(question_id=uuid4(), text=" ", confidence_value=0.9, reasoning_summary="reasoning")

def test_answer_empty_reasoning_raises_exception() -> None:
    with pytest.raises(ValidationException, match="Reasoning summary cannot be empty."):
        Answer.create(question_id=uuid4(), text="text", confidence_value=0.9, reasoning_summary="")

def test_create_valid_citation() -> None:
    c = Citation.create(
        answer_id=uuid4(),
        document_id=uuid4(),
        chunk_id=uuid4(),
        document_name="doc.pdf",
        excerpt="Paris is the capital of France.",
        page_number=1
    )
    assert c.document_name == "doc.pdf"

def test_citation_empty_excerpt_raises_exception() -> None:
    with pytest.raises(ValidationException, match="Excerpt cannot be empty."):
        Citation.create(
            answer_id=uuid4(),
            document_id=uuid4(),
            chunk_id=uuid4(),
            document_name="doc.pdf",
            excerpt="   "
        )
