from chunking import split_with_overlap


def test_overlap_preserves_boundary():
    chunks = split_with_overlap("one two three four five", 4, 2)
    assert chunks[0].split()[-2:] == chunks[1].split()[:2]
