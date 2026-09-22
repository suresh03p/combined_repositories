def test_expected_sources_are_defined():
    from retrieval_evaluation import QUESTIONS
    assert len(QUESTIONS) >= 10
