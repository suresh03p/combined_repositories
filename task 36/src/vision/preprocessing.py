from __future__ import annotations

from PIL import Image, ImageFilter, ImageEnhance


def resize_image(image, width=None, height=None):
    if width is None and height is None:
        return image.copy()
    if width is not None and height is None:
        ratio = width / image.width
        height = max(1, int(image.height * ratio))
    elif height is not None and width is None:
        ratio = height / image.height
        width = max(1, int(image.width * ratio))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def crop_image(image, box):
    return image.crop(box)


def rotate_image(image, angle=90):
    return image.rotate(angle, expand=True)


def grayscale_image(image):
    return image.convert("L")


def denoise_image(image):
    return image.filter(ImageFilter.MedianFilter(size=3))


def adjust_contrast(image, factor=1.5):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def preprocess_document(image, operations=None):
    result = image.copy()
    operations = operations or ["grayscale", "contrast", "resize"]
    for operation in operations:
        if operation == "grayscale":
            result = grayscale_image(result)
        elif operation == "contrast":
            result = adjust_contrast(result, factor=1.6)
        elif operation == "resize":
            result = resize_image(result, width=1600)
        elif operation == "denoise":
            result = denoise_image(result)
    return result


def preprocess_for_ocr(image):
    return preprocess_document(image, operations=["grayscale", "contrast", "denoise", "resize"])
