from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    source_title: str
    source_url: str
    excerpt: str


@dataclass(frozen=True)
class Candidate:
    claim: str
    evidence: tuple[Evidence, ...] = ()


@dataclass(frozen=True)
class CandidateResult:
    candidate_id: str
    claim: str
    status: str
    rejection_reason: str | None
    evidence: tuple[Evidence, ...]


@dataclass(frozen=True)
class RunResult:
    run_id: str
    query: str
    status: str
    candidates: tuple[CandidateResult, ...]
    created_at: str
