"""Metadata construction and safe filter matching."""
from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class ChunkMetadata:
    chunk_id: str
    document_id: str
    document_name: str
    page_number: int
    section: str = "Unknown"
    tenant_id: str = "company_a"
    access_level: str = "employee"
    document_type: str = "policy"
    department: str = "HR"

    def as_dict(self) -> dict:
        return asdict(self)


def make_metadata(document_name: str, page: int, index: int, **overrides) -> dict:
    document_id = document_name.rsplit(".", 1)[0]
    values = dict(chunk_id=f"{document_id}_{index:03d}", document_id=document_id,
                  document_name=document_name, page_number=page)
    values.update(overrides)
    return ChunkMetadata(**values).as_dict()


def matches_filter(metadata: dict, filters: dict | None) -> bool:
    return not filters or all(metadata.get(key) == value for key, value in filters.items())
