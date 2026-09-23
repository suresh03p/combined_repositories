import json
from pathlib import Path

from reportlab.pdfgen import canvas

from ingestion.document_loader import get_document_metadata, load_document, validate_document
from parsing.page_parser import parse_document, write_pages


def make_pdf(path: Path) -> None:
    pdf = canvas.Canvas(str(path))
    pdf.setTitle("Test document")
    pdf.drawString(50, 750, "Page one heading")
    pdf.showPage()
    pdf.drawString(50, 750, "Page two heading")
    pdf.save()


def test_metadata_and_page_numbers_are_preserved(tmp_path: Path) -> None:
    source = tmp_path / "sample.pdf"
    make_pdf(source)

    metadata = get_document_metadata(source)
    assert metadata["filename"] == "sample.pdf"
    assert metadata["file_type"] == "application/pdf"
    assert metadata["page_count"] == 2
    assert metadata["document_id"].startswith("DOC-")
    assert load_document(source)["document_id"] == metadata["document_id"]

    pages = parse_document(source)
    assert [page["page_number"] for page in pages] == [1, 2]
    assert all(page["document_id"] == metadata["document_id"] for page in pages)
    assert "Page one heading" in pages[0]["text"]

    output = write_pages(source, tmp_path / "pages")
    assert len(output) == 2
    assert json.loads(output[1].read_text(encoding="utf-8"))["page_number"] == 2


def test_validation_rejects_unsupported_files(tmp_path: Path) -> None:
    unsupported = tmp_path / "notes.txt"
    unsupported.write_text("not a PDF", encoding="utf-8")
    try:
        validate_document(unsupported)
    except ValueError as error:
        assert "Unsupported" in str(error)
    else:
        raise AssertionError("Expected unsupported file validation to fail")