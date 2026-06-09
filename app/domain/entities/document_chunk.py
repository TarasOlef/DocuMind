from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.exceptions.base import ValidationException
from app.domain.value_objects.metadata import ChunkMetadata


@dataclass
class DocumentChunk:
    id: UUID
    document_id: UUID
    content: str
    chunk_index: int
    page_number: int | None
    metadata: ChunkMetadata
    created_at: datetime

    def __post_init__(self) -> None:
        if not self.content or not self.content.strip():
            raise ValidationException("Chunk content cannot be empty.")
        if self.chunk_index < 0:
            raise ValidationException("Chunk index cannot be negative.")
        if self.page_number is not None and self.page_number <= 0:
            raise ValidationException("Page number must be greater than 0.")

    @classmethod
    def create(
        cls,
        document_id: UUID,
        content: str,
        chunk_index: int,
        page_number: int | None = None,
        metadata: ChunkMetadata | None = None,
    ) -> "DocumentChunk":
        return cls(
            id=uuid4(),
            document_id=document_id,
            content=content.strip(),
            chunk_index=chunk_index,
            page_number=page_number,
            metadata=metadata or {},
            created_at=datetime.now(timezone.utc),
        )

    def excerpt(self, max_length: int = 250) -> str:
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length].rsplit(' ', 1)[0] + '...'
