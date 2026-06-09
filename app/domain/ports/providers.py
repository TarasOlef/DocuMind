from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from app.domain.entities.document_chunk import DocumentChunk


class LLMProviderPort(Protocol):
    async def generate_answer(
        self,
        question: str,
        context: str,
        instructions: str,
    ) -> str: ...

class EmbeddingProviderPort(Protocol):
    async def embed_text(self, text: str) -> list[float]: ...
    async def embed_texts(self, texts: list[str]) -> list[list[float]]: ...

class DocumentTextExtractorPort(Protocol):
    async def extract_text(self, file_path: str) -> str: ...

@dataclass(frozen=True)
class VectorSearchResult:
    chunk: DocumentChunk
    score: float

class VectorSearchPort(Protocol):
    async def search_similar_chunks(
        self,
        query_embedding: list[float],
        user_id: UUID,
        organization_id: UUID | None,
        document_ids: list[UUID] | None = None,
        top_k: int = 5,
        min_score: float = 0.0,
    ) -> list[VectorSearchResult]: ...
