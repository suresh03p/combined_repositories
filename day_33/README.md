# Enterprise Document Intelligence

This exercise demonstrates why plain-text extraction is insufficient for enterprise documents. A product table, its page number, the heading above it, and a chart image are separate signals that must remain linked for retrieval and answer citations.

## Pipeline

```text
PDF -> document metadata -> pages -> sections/headings/paragraph positions/tables/images
    -> data/processed/pages/*.json -> layout-aware chunks -> embeddings -> retrieval
```

The parser keeps 1-based source page numbers and a deterministic `document_id`. Each page JSON contains `document_id`, `page_number`, `text`, `section`, `heading`, `paragraphs` with bounding-box positions, `tables`, and `images`.

## Setup and run

```powershell
py -m pip install -r requirements.txt
py scripts/create_sample_dataset.py
py scripts/ingest_dataset.py
py -m pytest
```

The sample PDFs are generated locally from original text and graphics, so they are safe for training/testing and do not depend on third-party copyrighted documents. For real data, record the source, license/permission, acquisition date, and any personal-data review in `data/raw/dataset_manifest.json` before ingestion.

## Learning checkpoints

Traditional RAG flattens `Document -> Plain Text -> Chunks`, which can make a table row look unrelated to its header or a chart lose its caption. Layout-aware RAG retains `Pages -> Sections -> Tables -> Images -> Metadata` before creating multimodal chunks, allowing retrieval to preserve page citations and relationships.