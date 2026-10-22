import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

from .models import Candidate, CandidateResult, Evidence, RunResult


class SQLiteStore:
    def __init__(self, database_path: str | Path):
        self._database_path = str(database_path)
        if not self._database_path or self._database_path == ":memory:":
            raise ValueError("A file-backed SQLite database path is required.")
        Path(self._database_path).parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as connection:
            connection.executescript(
                """
                PRAGMA foreign_keys = ON;
                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    query TEXT NOT NULL,
                    status TEXT NOT NULL CHECK (status = 'completed'),
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS candidates (
                    candidate_id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL REFERENCES runs(run_id),
                    claim TEXT NOT NULL,
                    status TEXT NOT NULL CHECK (
                        status IN (
                            'pending_review',
                            'rejected_unsupported',
                            'approved',
                            'rejected_by_reviewer'
                        )
                    ),
                    rejection_reason TEXT
                );
                CREATE TABLE IF NOT EXISTS evidence (
                    candidate_id TEXT NOT NULL REFERENCES candidates(candidate_id),
                    position INTEGER NOT NULL,
                    source_title TEXT NOT NULL,
                    source_url TEXT NOT NULL,
                    excerpt TEXT NOT NULL,
                    PRIMARY KEY (candidate_id, position)
                );
                CREATE TABLE IF NOT EXISTS reviews (
                    candidate_id TEXT PRIMARY KEY REFERENCES candidates(candidate_id),
                    reviewer TEXT NOT NULL,
                    decision TEXT NOT NULL CHECK (decision IN ('approved', 'rejected')),
                    rationale TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path, timeout=5)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def save_run(
        self,
        run_id: str,
        query: str,
        candidates: list[tuple[str, Candidate, str | None]],
    ) -> None:
        created_at = datetime.now(timezone.utc).isoformat()
        with closing(self._connect()) as connection:
            with connection:
                connection.execute(
                    "INSERT INTO runs (run_id, query, status, created_at) "
                    "VALUES (?, ?, 'completed', ?)",
                    (run_id, query, created_at),
                )
                for candidate_id, candidate, rejection_reason in candidates:
                    status = (
                        "rejected_unsupported"
                        if rejection_reason is not None
                        else "pending_review"
                    )
                    connection.execute(
                        """
                        INSERT INTO candidates (
                            candidate_id, run_id, claim, status, rejection_reason
                        ) VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            candidate_id,
                            run_id,
                            candidate.claim,
                            status,
                            rejection_reason,
                        ),
                    )
                    for position, item in enumerate(candidate.evidence):
                        connection.execute(
                            """
                            INSERT INTO evidence (
                                candidate_id, position, source_title, source_url, excerpt
                            ) VALUES (?, ?, ?, ?, ?)
                            """,
                            (
                                candidate_id,
                                position,
                                item.source_title,
                                item.source_url,
                                item.excerpt,
                            ),
                        )

    def get_run(self, run_id: str) -> RunResult:
        with closing(self._connect()) as connection:
            run = connection.execute(
                "SELECT run_id, query, status, created_at FROM runs WHERE run_id = ?",
                (run_id,),
            ).fetchone()
            if run is None:
                raise KeyError(f"Unknown research run: {run_id}")

            rows = connection.execute(
                """
                SELECT candidate_id, claim, status, rejection_reason
                FROM candidates
                WHERE run_id = ?
                ORDER BY rowid
                """,
                (run_id,),
            ).fetchall()
            results = tuple(
                CandidateResult(
                    candidate_id=row["candidate_id"],
                    claim=row["claim"],
                    status=row["status"],
                    rejection_reason=row["rejection_reason"],
                    evidence=self._get_evidence(connection, row["candidate_id"]),
                )
                for row in rows
            )

        return RunResult(
            run_id=run["run_id"],
            query=run["query"],
            status=run["status"],
            candidates=results,
            created_at=run["created_at"],
        )

    def review_candidate(
        self,
        run_id: str,
        candidate_id: str,
        reviewer: str,
        approved: bool,
        rationale: str,
    ) -> CandidateResult:
        decision = "approved" if approved else "rejected"
        updated_status = "approved" if approved else "rejected_by_reviewer"
        with closing(self._connect()) as connection:
            with connection:
                row = connection.execute(
                    """
                    SELECT status FROM candidates
                    WHERE candidate_id = ? AND run_id = ?
                    """,
                    (candidate_id, run_id),
                ).fetchone()
                if row is None:
                    raise KeyError(f"Unknown candidate {candidate_id} in run {run_id}")
                if row["status"] != "pending_review":
                    raise ValueError(
                        f"Candidate cannot be reviewed from status {row['status']}."
                    )

                connection.execute(
                    "UPDATE candidates SET status = ? WHERE candidate_id = ?",
                    (updated_status, candidate_id),
                )
                connection.execute(
                    """
                    INSERT INTO reviews (
                        candidate_id, reviewer, decision, rationale, created_at
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        candidate_id,
                        reviewer,
                        decision,
                        rationale,
                        datetime.now(timezone.utc).isoformat(),
                    ),
                )
                result_row = connection.execute(
                    """
                    SELECT candidate_id, claim, status, rejection_reason
                    FROM candidates WHERE candidate_id = ?
                    """,
                    (candidate_id,),
                ).fetchone()
                evidence = self._get_evidence(connection, candidate_id)

        return CandidateResult(
            candidate_id=result_row["candidate_id"],
            claim=result_row["claim"],
            status=result_row["status"],
            rejection_reason=result_row["rejection_reason"],
            evidence=evidence,
        )

    @staticmethod
    def _get_evidence(
        connection: sqlite3.Connection, candidate_id: str
    ) -> tuple[Evidence, ...]:
        rows = connection.execute(
            """
            SELECT source_title, source_url, excerpt
            FROM evidence
            WHERE candidate_id = ?
            ORDER BY position
            """,
            (candidate_id,),
        ).fetchall()
        return tuple(
            Evidence(
                source_title=row["source_title"],
                source_url=row["source_url"],
                excerpt=row["excerpt"],
            )
            for row in rows
        )
