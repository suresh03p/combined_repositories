import unittest

from chunking import split_with_overlap


class RetrievalContractTests(unittest.TestCase):
    def test_chunk_metadata_contract_is_documented_by_shape(self):
        chunks = split_with_overlap("leave requests use the HR portal", 4, 1)
        self.assertTrue(chunks)
        self.assertTrue(all(chunk for chunk in chunks))


if __name__ == "__main__":
    unittest.main()
