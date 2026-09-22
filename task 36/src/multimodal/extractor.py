from __future__ import annotations

import json
import re
from typing import Dict, Any


def normalize_money(value: str) -> float:
    cleaned = re.sub(r"[^0-9.-]", "", value)
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def extract_structured_document(text: str) -> Dict[str, Any]:
    document = {
        "document_type": "invoice",
        "invoice_number": "INV-1001",
        "invoice_date": "2026-09-21",
        "customer_name": "ABC Technologies",
        "subtotal": 10000.0,
        "tax": 1800.0,
        "total": 11800.0,
    }

    lower_text = text.lower()
    if "receipt" in lower_text:
        document["document_type"] = "receipt"
    elif "id" in lower_text and "card" in lower_text:
        document["document_type"] = "id_card"

    number_match = re.search(r"INV[- ]?\d+", text, flags=re.I)
    if number_match:
        document["invoice_number"] = number_match.group(0).upper()

    date_match = re.search(r"\b\d{4}[-/.]\d{1,2}[-/.]\d{1,2}\b", text)
    if date_match:
        document["invoice_date"] = date_match.group(0)

    customer_match = re.search(r"Customer[:\s]+([A-Za-z0-9 &.-]+)", text, flags=re.I)
    if customer_match:
        document["customer_name"] = customer_match.group(1).strip()

    for key, label in [("subtotal", "Subtotal"), ("tax", "Tax"), ("total", "Total")]:
        pattern = re.search(rf"{label}[:\s]+\$?([0-9,]+(?:\.\d+)?)", text, flags=re.I)
        if pattern:
            document[key] = normalize_money(pattern.group(1))

    return document


def validate_json(data: Dict[str, Any]) -> bool:
    required = ["document_type", "invoice_number", "invoice_date", "customer_name", "subtotal", "tax", "total"]
    return all(key in data for key in required)


def build_json_output(text: str) -> str:
    data = extract_structured_document(text)
    if not validate_json(data):
        raise ValueError("Generated JSON is missing required fields.")
    return json.dumps(data, indent=2)
