import unittest

from chunking import split_into_chunks, split_with_overlap


class ChunkingTests(unittest.TestCase):
    def test_plain_chunks_have_requested_maximum_size(self):
        chunks = split_into_chunks("one two three four five six seven", 3)
        self.assertEqual([3, 3, 1], [len(chunk.split()) for chunk in chunks])

    def test_overlap_repeats_boundary_words(self):
        chunks = split_with_overlap("one two three four five six", 4, 2)
        self.assertEqual(chunks[0].split()[-2:], chunks[1].split()[:2])

    def test_overlap_must_be_smaller_than_chunk(self):
        with self.assertRaises(ValueError):
            split_with_overlap("one two", 2, 2)


if __name__ == "__main__":
    unittest.main()
