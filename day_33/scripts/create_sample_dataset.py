"""Generate a small synthetic dataset with no external document rights risk."""

from pathlib import Path

from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


RAW = Path("data/raw")


def _pdf(path: Path, title: str, lines: list[str], table: bool = False, image: bool = False) -> None:
    pdf = canvas.Canvas(str(path), pagesize=letter)
    pdf.setTitle(title)
    pdf.setAuthor("Synthetic Enterprise Document Intelligence Dataset")
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(54, 740, title)
    pdf.setFont("Helvetica", 11)
    y = 705
    for line in lines:
        pdf.drawString(54, y, line)
        y -= 18
    if table:
        y -= 14
        rows = [("Item", "Quantity", "Amount"), ("Widget A", "12", "$1,200"), ("Widget B", "4", "$800")]
        for row in rows:
            x = 54
            for value in row:
                pdf.rect(x, y - 5, 150, 22)
                pdf.drawString(x + 6, y + 2, value)
                x += 150
            y -= 22
    if image:
        image_path = path.with_suffix(".png")
        canvas_image = Image.new("RGB", (500, 180), "white")
        draw = ImageDraw.Draw(canvas_image)
        draw.rectangle((30, 30, 470, 150), outline="black", width=3)
        draw.line((50, 130, 150, 100, 250, 120, 350, 65, 450, 85), fill="blue", width=4)
        draw.text((45, 40), "Synthetic trend chart", fill="black")
        canvas_image.save(image_path)
        pdf.drawImage(ImageReader(str(image_path)), 54, 420, width=400, height=144)
        image_path.unlink()
    pdf.save()


def _scanned(path: Path, title: str) -> None:
    image = Image.new("RGB", (1275, 1650), "white")
    draw = ImageDraw.Draw(image)
    draw.text((100, 120), title, fill="black")
    draw.text((100, 220), "Synthetic scanned page for OCR testing", fill="black")
    image.save(path, "PDF", resolution=150.0)


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    _pdf(RAW / "general_policy.pdf", "Operations Policy", ["Customer information", "Policy revision: 2026"])
    _pdf(RAW / "general_catalog.pdf", "Product Catalog", ["Product information", "Catalog section 1"], image=True)
    _pdf(RAW / "general_summary.pdf", "Quarterly Summary", ["Financial summary", "Prepared for internal testing"], table=True)
    _scanned(RAW / "scanned_receipt.pdf", "Scanned Receipt")
    _scanned(RAW / "scanned_form.pdf", "Scanned Customer Form")
    _pdf(RAW / "invoice_001.pdf", "Invoice 001", ["Bill to: Synthetic Customer", "Terms: Net 30"], table=True)
    _pdf(RAW / "invoice_002.pdf", "Invoice 002", ["Bill to: Example Organization", "Terms: Net 15"], table=True)
    _pdf(RAW / "financial_report.pdf", "Financial Report", ["Financial summary", "Revenue and operating expenses"], table=True, image=True)
    _pdf(RAW / "product_document.pdf", "Product Specification", ["Product overview", "Technical specifications"], image=True)

    manifest = RAW / "dataset_manifest.json"
    manifest.write_text(
        '{\n'
        '  "rights_status": "synthetic_original_content",\n'
        '  "permission": "Generated locally by this repository for training and testing.",\n'
        '  "source": "create_sample_dataset.py",\n'
        '  "acquired_at": "2026-09-23",\n'
        '  "personal_data_review": "No real personal data; placeholder names only."\n'
        '}\n',
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()