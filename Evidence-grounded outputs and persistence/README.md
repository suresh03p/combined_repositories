# Evidence-grounded research outputs

A dependency-free Python example for recording candidate research results with source provenance and durable review state. It accepts outputs from an upstream research step; it does not perform web search or generate claims itself.

## Decisions and behavior

- A candidate is eligible for review only when it has a non-empty claim and at least one evidence item with a title, excerpt, and absolute HTTP(S) URL.
- Unsupported or malformed candidates are retained as `rejected_unsupported` results with a reason. Supplied source fields, including rejected URLs, are preserved for audit.
- Valid candidates start at `pending_review`. A separate reviewer action can approve or reject them; it cannot review unsupported results or repeat a completed decision.
- A run, its candidates, and all supplied evidence are written in one SQLite transaction. Reviewer decisions and state transitions are also atomic.
- There is no outreach action or integration. Approval records a human review decision only; it does not send messages or contact candidates.

The URL and excerpt checks are structural, not semantic. They do not prove that a source is trustworthy, current, or actually supports the claim. Human reviewers must check those points before approving. Source availability is not checked, and the URL is stored exactly as supplied.

## Run and test

From this directory, with Python 3.10 or later:

```powershell
python -m unittest discover -s tests -v
```

Example use:

```python
from research_pipeline import Candidate, Evidence, ResearchPipeline, SQLiteStore

pipeline = ResearchPipeline(SQLiteStore("outputs/research.sqlite3"))
run = pipeline.record_run(
    "Research question",
    (
        Candidate(
            "Candidate claim to verify.",
            (
                Evidence(
                    "Source title",
                    "https://source.example/document",
                    "Relevant source excerpt",
                ),
            ),
        ),
        Candidate("Candidate with no evidence."),
    ),
)
```

`run.candidates` contains both outcomes: the first enters `pending_review`, while the second is `rejected_unsupported`. Review a supported result separately:

```python
reviewed = pipeline.review_candidate(
    run.run_id,
    run.candidates[0].candidate_id,
    reviewer="reviewer-id",
    approved=True,
    rationale="Checked the source against the claim.",
)
```

The example URL is a placeholder; use the original source URL and a faithful excerpt in real runs. The database file is created at the supplied path. No external dependencies or network calls are required.

## Known limitations

- The project records upstream research; it does not retrieve sources, evaluate evidence relevance, or detect fabricated quotations.
- Approval is a recorded state, not a guarantee of factual correctness or authorization for outreach.
- SQLite supports a local, single-process example. Authentication, multi-user review authorization, retention controls, and tamper-evident audit history are outside this demo.
