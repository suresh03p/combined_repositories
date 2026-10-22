from urllib.parse import urlsplit
from uuid import uuid4

from .models import Candidate, CandidateResult, Evidence, RunResult
from .store import SQLiteStore


def _rejection_reason(candidate: Candidate) -> str | None:
    if not isinstance(candidate.claim, str) or not candidate.claim.strip():
        return "Claim is empty."
    if not candidate.evidence:
        return "No source evidence supplied."

    for item in candidate.evidence:
        if not isinstance(item, Evidence):
            return "Evidence must include a source title, URL, and excerpt."
        if not all(
            isinstance(value, str) and value.strip()
            for value in (item.source_title, item.source_url, item.excerpt)
        ):
            return "Evidence must include a source title, URL, and excerpt."
        try:
            parsed = urlsplit(item.source_url)
            valid_url = (
                parsed.scheme.lower() in {"http", "https"}
                and parsed.hostname is not None
                and not any(character.isspace() for character in item.source_url)
            )
        except ValueError:
            valid_url = False
        if not valid_url:
            return "Evidence URL must be an absolute HTTP(S) URL."

    return None


class ResearchPipeline:
    """Persists research candidates for review without performing outreach."""

    def __init__(self, store: SQLiteStore):
        self._store = store

    def record_run(self, query: str, candidates: tuple[Candidate, ...]) -> RunResult:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Research query must not be empty.")

        prepared: list[tuple[str, Candidate, str | None]] = []
        for candidate in candidates:
            if not isinstance(candidate, Candidate):
                raise TypeError("Each candidate must be a Candidate.")
            if not isinstance(candidate.claim, str):
                raise TypeError("Candidate claim must be a string.")
            try:
                evidence = tuple(candidate.evidence)
            except TypeError as error:
                raise TypeError("Candidate evidence must be iterable.") from error
            if any(not isinstance(item, Evidence) for item in evidence):
                raise TypeError("Each evidence item must be an Evidence.")
            if any(
                not isinstance(value, str)
                for item in evidence
                for value in (item.source_title, item.source_url, item.excerpt)
            ):
                raise TypeError("Evidence title, URL, and excerpt must be strings.")

            normalized = Candidate(candidate.claim, evidence)
            prepared.append(
                (str(uuid4()), normalized, _rejection_reason(normalized))
            )

        run_id = str(uuid4())
        self._store.save_run(run_id, query, prepared)
        return self._store.get_run(run_id)

    def get_run(self, run_id: str) -> RunResult:
        return self._store.get_run(run_id)

    def review_candidate(
        self,
        run_id: str,
        candidate_id: str,
        reviewer: str,
        approved: bool,
        rationale: str = "",
    ) -> CandidateResult:
        if not isinstance(reviewer, str) or not reviewer.strip():
            raise ValueError("Reviewer must not be empty.")
        if not isinstance(approved, bool):
            raise TypeError("approved must be a bool.")
        if not isinstance(rationale, str):
            raise TypeError("rationale must be a string.")

        return self._store.review_candidate(
            run_id,
            candidate_id,
            reviewer.strip(),
            approved,
            rationale,
        )
