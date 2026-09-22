from __future__ import annotations

from typing import Dict, Any


def analyze_image(image_path: str, prompt: str) -> Dict[str, Any]:
    """Simulated vision analysis response for plugin-free local usage."""
    prompt_lower = prompt.lower()
    image_type = "invoice"
    if "receipt" in prompt_lower:
        image_type = "receipt"
    elif "id" in prompt_lower or "card" in prompt_lower:
        image_type = "id card"
    elif "screenshot" in prompt_lower:
        image_type = "screenshot"

    response = {
        "image_path": image_path,
        "document_type": image_type,
        "summary": "The image appears to contain a document with text and layout structures.",
        "text_visible": "Visible text includes invoice number, customer name, date, and total amount.",
        "objects_present": ["document", "text fields", "table or form area"],
        "prompt": prompt,
    }
    return response
