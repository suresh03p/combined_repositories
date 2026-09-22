from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Any, Dict, List, Sequence

from utils import deduplicate_records, validate_record


def _filter_valid_records(records: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [record for record in records if validate_record(record)]


def _deduplicate_records(records: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return deduplicate_records(records)


class DataProcessor:
    def __init__(self) -> None:
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        self.process_pool = ProcessPoolExecutor(max_workers=2)

    def process_payloads(self, payloads: Sequence[Any]) -> List[Dict[str, Any]]:
        flattened: List[Dict[str, Any]] = []
        for payload in payloads:
            if isinstance(payload, list):
                flattened.extend([item for item in payload if isinstance(item, dict)])
            elif isinstance(payload, dict):
                flattened.append(payload)

        valid_future = self.thread_pool.submit(_filter_valid_records, flattened)
        valid_records = valid_future.result()
        unique_future = self.process_pool.submit(_deduplicate_records, valid_records)
        return unique_future.result()

    def aggregate(self, records: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "total_records": len(records),
            "record_keys": sorted({key for record in records for key in record.keys()}),
        }

    def shutdown(self) -> None:
        self.thread_pool.shutdown(wait=True)
        self.process_pool.shutdown(wait=True)
