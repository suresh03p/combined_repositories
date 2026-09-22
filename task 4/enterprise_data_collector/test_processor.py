from processor import DataProcessor


def test_process_payloads_deduplicates_and_filters() -> None:
    processor = DataProcessor()
    payloads = [
        [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}, {"id": 1, "name": "A"}],
        {"id": 3, "name": "C"},
    ]
    records = processor.process_payloads(payloads)
    assert len(records) == 3
    assert records[0]["id"] == 1
    processor.shutdown()
