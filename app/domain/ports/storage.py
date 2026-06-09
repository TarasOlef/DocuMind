from typing import Protocol
from uuid import UUID


class DocumentStoragePort(Protocol):
    async def save_file(
        self,
        filename: str,
        content: bytes,
        owner_id: UUID,
    ) -> str: ...

    async def delete_file(self, storage_path: str) -> None: ...

    async def exists(self, storage_path: str) -> bool: ...
