from enum import Enum

from app.domain.exceptions.document_exceptions import InvalidFileTypeException


class FileType(str, Enum):
    PDF = "pdf"
    TXT = "txt"

def file_type_from_filename(filename: str) -> FileType:
    """Extract and validate the file type from a filename."""
    if "." not in filename:
        raise InvalidFileTypeException(f"Filename '{filename}' has no extension.")

    ext = filename.rsplit(".", 1)[-1].lower()
    try:
        return FileType(ext)
    except ValueError:
        raise InvalidFileTypeException(f"File extension '.{ext}' is not supported.") from None
