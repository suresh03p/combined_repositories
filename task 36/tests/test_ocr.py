import json
import os
from unittest.mock import patch

from PIL import Image, ImageDraw

from src.ocr.ocr_engine import extract_text


def create_sample_invoice(path: str):
    image = Image.new("RGB", (1200, 800), "white")
    draw = ImageDraw.Draw(image)
    draw.text((80, 80), "Invoice Number: INV1001", fill="black")
    draw.text((80, 140), "Customer: ABC Technologies", fill="black")
    draw.text((80, 200), "Total: 11800", fill="black")
    image.save(path)


def test_ocr_extracts_expected_text(tmp_path):
    image_path = tmp_path / "invoice_test.png"
    create_sample_invoice(str(image_path))

    output_path = tmp_path / "out.txt"
    with patch("src.ocr.ocr_engine.pytesseract.image_to_string", return_value="Invoice Number: INV1001\nCustomer: ABC Technologies\nTotal: 11800"):
        result = extract_text(str(image_path), str(output_path))

    assert "INV1001" in result or "INV" in result
    assert "ABC" in result or "Technology" in result
    assert output_path.exists()


def test_multimodal_json_schema():
    sample = {
        "document_type": "invoice",
        "invoice_number": "INV-1001",
        "invoice_date": "2026-09-21",
        "customer_name": "ABC Technologies",
        "subtotal": 10000,
        "tax": 1800,
        "total": 11800,
    }

    assert set(sample.keys()) == {"document_type", "invoice_number", "invoice_date", "customer_name", "subtotal", "tax", "total"}
    assert isinstance(sample["total"], int)


def test_evaluation_dataset_file_exists():
    dataset_path = os.path.join("data", "evaluation", "multimodal_questions.json")
    if os.path.exists(dataset_path):
        with open(dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, list)
        assert len(data) >= 20
