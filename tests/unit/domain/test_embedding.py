from uuid import uuid4

import pytest

from app.domain.entities.embedding import Embedding
from app.domain.exceptions.base import ValidationException


def test_create_valid_embedding_for_chunk() -> None:
    chunk_id = uuid4()
    emb = Embedding.create_for_chunk(
        chunk_id=chunk_id,
        vector=[0.1, 0.2, 0.3],
        model="test-model"
    )
    assert emb.chunk_id == chunk_id
    assert emb.question_id is None
    assert emb.dimension == 3

def test_embedding_empty_vector_raises_exception() -> None:
    with pytest.raises(ValidationException, match="Embedding vector cannot be empty."):
        Embedding.create_for_chunk(chunk_id=uuid4(), vector=[], model="test-model")

def test_embedding_dimension_mismatch_raises_exception() -> None:
    with pytest.raises(ValidationException, match="Dimension 5 does not match vector length 2."):
        Embedding(
            id=uuid4(),
            vector=[0.1, 0.2],
            model="test-model",
            dimension=5,
            chunk_id=uuid4(),
            question_id=None,
            created_at=None # type: ignore
        )

def test_embedding_empty_model_raises_exception() -> None:
    with pytest.raises(ValidationException, match="Model name cannot be empty."):
        Embedding.create_for_chunk(chunk_id=uuid4(), vector=[0.1], model="   ")

def test_embedding_both_chunk_and_question_raises_exception() -> None:
    with pytest.raises(ValidationException, match="Embedding must belong to either a chunk or a question, but not both."):
        Embedding(
            id=uuid4(),
            vector=[0.1],
            model="test",
            dimension=1,
            chunk_id=uuid4(),
            question_id=uuid4(),
            created_at=None # type: ignore
        )
