import pytest

from app.domain.exceptions.document_exceptions import InvalidFileTypeException
from app.domain.value_objects.file_type import FileType, file_type_from_filename


def test_file_type_from_filename_pdf() -> None:
    assert file_type_from_filename("document.pdf") == FileType.PDF
    assert file_type_from_filename("document.PDF") == FileType.PDF

def test_file_type_from_filename_txt() -> None:
    assert file_type_from_filename("notes.txt") == FileType.TXT

def test_file_type_from_filename_invalid_extension() -> None:
    with pytest.raises(InvalidFileTypeException, match="File extension '.docx' is not supported."):
        file_type_from_filename("document.docx")

def test_file_type_from_filename_no_extension() -> None:
    with pytest.raises(InvalidFileTypeException, match="Filename 'document' has no extension."):
        file_type_from_filename("document")
