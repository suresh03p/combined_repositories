import tempfile
import unittest
from pathlib import Path

from research_pipeline import Candidate, Evidence, ResearchPipeline, SQLiteStore


class ResearchPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        database_path = Path(self.temp_dir.name) / "research.sqlite3"
        self.pipeline = ResearchPipeline(SQLiteStore(database_path))

    def test_valid_candidate_and_source_provenance_survive_reload(self):
        source = Evidence(
            source_title="Example source",
            source_url="https://example.org/report?id=1",
            excerpt="The source passage associated with the claim.",
        )

        result = self.pipeline.record_run(
            "Research topic",
            (Candidate("A source-backed claim.", (source,)),),
        )
        reloaded = self.pipeline.get_run(result.run_id)

        self.assertEqual(reloaded.status, "completed")
        self.assertEqual(len(reloaded.candidates), 1)
        self.assertEqual(reloaded.candidates[0].status, "pending_review")
        self.assertEqual(reloaded.candidates[0].evidence, (source,))

    def test_unsupported_and_malformed_candidates_are_rejected_and_persisted(self):
        malformed_source = Evidence(
            source_title="Unresolvable source",
            source_url="javascript:alert(1)",
            excerpt="An excerpt is not enough when its citation is invalid.",
        )
        result = self.pipeline.record_run(
            "Research topic",
            (
                Candidate("A claim with no support."),
                Candidate("A claim with an invalid citation.", (malformed_source,)),
            ),
        )

        unsupported, malformed = result.candidates
        self.assertEqual(unsupported.status, "rejected_unsupported")
        self.assertEqual(unsupported.rejection_reason, "No source evidence supplied.")
        self.assertEqual(malformed.status, "rejected_unsupported")
        self.assertEqual(
            malformed.rejection_reason,
            "Evidence URL must be an absolute HTTP(S) URL.",
        )
        self.assertEqual(malformed.evidence[0].source_url, "javascript:alert(1)")
        self.assertEqual(len(self.pipeline.get_run(result.run_id).candidates), 2)

    def test_review_is_separate_and_rejected_candidates_cannot_be_approved(self):
        result = self.pipeline.record_run(
            "Research topic",
            (
                Candidate(
                    "A supported claim.",
                    (Evidence("Source", "https://example.org/source", "A quoted excerpt."),),
                ),
                Candidate("An unsupported claim."),
            ),
        )
        supported, unsupported = result.candidates

        self.assertEqual(supported.status, "pending_review")
        approved = self.pipeline.review_candidate(
            result.run_id, supported.candidate_id, "reviewer-1", True, "Verified."
        )
        self.assertEqual(approved.status, "approved")
        with self.assertRaises(ValueError):
            self.pipeline.review_candidate(
                result.run_id, supported.candidate_id, "reviewer-1", True
            )
        with self.assertRaises(ValueError):
            self.pipeline.review_candidate(
                result.run_id, unsupported.candidate_id, "reviewer-1", True
            )

    def test_empty_query_is_rejected_before_persistence(self):
        with self.assertRaises(ValueError):
            self.pipeline.record_run("  ", ())


if __name__ == "__main__":
    unittest.main()
