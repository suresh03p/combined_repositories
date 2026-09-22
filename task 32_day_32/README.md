# Day 32 - Multimodal AI Document Intelligence

This project demonstrates a production-oriented multimodal document intelligence workflow using Python, OCR, image processing, and a FastAPI service for document analysis.

## Project Overview

The application accepts an image or document plus a user question and returns a grounded answer based on OCR, visual analysis, and structured extraction.

## Architecture

- Image preprocessing and analysis
- OCR extraction
- Structured document parsing
- Multimodal retrieval and grounding
- FastAPI API with secure uploads
- Docker deployment support

## Installation

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Environment Variables

Copy `.env.example` to `.env` and update values as needed.

## OCR Pipeline

1. Load image
2. Preprocess image
3. Run OCR
4. Clean extracted text
5. Save output to `data/extracted_text`

## Vision Pipeline

1. Read image
2. Extract metadata and dimensions
3. Preprocess for OCR or analysis
4. Run prompt-based image understanding

## Multimodal RAG

The system can retrieve relevant context and produce grounded answers based on the document content rather than inventing missing values.

## API Documentation

Run:

```bash
uvicorn src.api.main:app --reload
```

Then open:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

## Testing

```bash
pytest -q
```

## Evaluation Results

Reports are stored in `outputs/`.

## Performance

See `outputs/performance_report.json`.

## Security

- Validate file types and size
- Reject unsupported extensions and malformed files
- Do not expose stack traces through the API

## Docker Deployment

```bash
docker compose up --build
```

## Limitations

This project is intentionally lightweight and does not ship large model files or private documents.

## Future Improvements

- Add a real vision-language model backend
- Add vector search and embeddings
- Expand dataset coverage and evaluation metrics
