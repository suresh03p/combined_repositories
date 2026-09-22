from __future__ import annotations

import os
from typing import Dict, Any

from PIL import Image


def load_image(image_path: str) -> Image.Image:
    """Open an image file and return a PIL image object."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    with Image.open(image_path) as img:
        return img.copy()


def resize_image(image: Image.Image, width: int = None, height: int = None, maintain_aspect_ratio: bool = True) -> Image.Image:
    """Resize an image while optionally preserving aspect ratio."""
    if width is None and height is None:
        return image.copy()

    if maintain_aspect_ratio:
        if width is not None and height is None:
            ratio = width / image.width
            height = max(1, int(image.height * ratio))
        elif height is not None and width is None:
            ratio = height / image.height
            width = max(1, int(image.width * ratio))
        elif width is not None and height is not None:
            ratio = min(width / image.width, height / image.height)
            width = max(1, int(image.width * ratio))
            height = max(1, int(image.height * ratio))

    return image.resize((width, height), Image.Resampling.LANCZOS)


def convert_image(image: Image.Image, mode: str = "RGB") -> Image.Image:
    """Convert image color mode."""
    return image.convert(mode)


def save_image(image: Image.Image, output_path: str, format_name: str = None) -> str:
    """Save image to disk and return the saved path."""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    image.save(output_path, format=format_name)
    return output_path


def get_image_metadata(image_path: str) -> Dict[str, Any]:
    """Return key metadata for an image file."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    with Image.open(image_path) as image:
        stats = os.stat(image_path)
        metadata = {
            "filename": os.path.basename(image_path),
            "width": image.width,
            "height": image.height,
            "format": image.format or "Unknown",
            "color_mode": image.mode,
            "file_size": stats.st_size,
        }
        return metadata


def report_image(image_path: str) -> Dict[str, Any]:
    """Return a simple structured summary for a given image."""
    return get_image_metadata(image_path)
