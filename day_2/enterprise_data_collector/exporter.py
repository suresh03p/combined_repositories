import json
import os
from pathlib import Path
from typing import Any, Dict, List, Sequence

from utils import write_csv, write_json


class ReportExporter:
    def __init__(self, reports_dir: str, data_dir: str) -> None:
        self.reports_dir = Path(reports_dir)
        self.data_dir = Path(data_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def export_reports(self, reports: Dict[str, Any], records: Sequence[Dict[str, Any]]) -> None:
        self._write_report_json(reports)
        self._write_records_json(records)
        self._write_records_csv(records)

    def _write_report_json(self, reports: Dict[str, Any]) -> None:
        write_json(str(self.reports_dir / "reports.json"), reports)

    def _write_records_json(self, records: Sequence[Dict[str, Any]]) -> None:
        write_json(str(self.data_dir / "processed_records.json"), list(records))

    def _write_records_csv(self, records: Sequence[Dict[str, Any]]) -> None:
        write_csv(str(self.data_dir / "processed_records.csv"), list(records))
