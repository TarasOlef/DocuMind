from uuid import uuid4

import pytest

from app.domain.entities.document_chunk import DocumentChunk
from app.domain.exceptions.base import ValidationException


def test_create_valid_document_chunk() -> None:
    chunk = DocumentChunk.create(
        document_id=uuid4(),
        content="This is a test chunk.",
        chunk_index=0,
        page_number=1
    )
    assert chunk.content == "This is a test chunk."
    assert chunk.chunk_index == 0
    assert chunk.page_number == 1

def test_document_chunk_empty_content_raises_exception() -> None:
    with pytest.raises(ValidationException, match="Chunk content cannot be empty."):
        DocumentChunk.create(
            document_id=uuid4(),
            content="   ",
            chunk_index=0
        )

def test_document_chunk_negative_index_raises_exception() -> None:
    with pytest.raises(ValidationException, match="Chunk index cannot be negative."):
        DocumentChunk.create(
            document_id=uuid4(),
            content="content",
            chunk_index=-1
        )

def test_document_chunk_zero_page_raises_exception() -> None:
    with pytest.raises(ValidationException, match="Page number must be greater than 0."):
        DocumentChunk.create(
            document_id=uuid4(),
            content="content",
            chunk_index=0,
            page_number=0
        )

def test_document_chunk_excerpt() -> None:
    chunk = DocumentChunk.create(
        document_id=uuid4(),
        content="This is a very long string that will be cut off by the excerpt method if we pass a short length.",
        chunk_index=0
    )

    assert chunk.excerpt(100) == chunk.content
    assert chunk.excerpt(20).endswith("...")
    assert len(chunk.excerpt(20)) <= 23
