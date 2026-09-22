from pathlib import Path
from typing import Any, Dict, Sequence

from utils import write_csv, write_json


class ReportExporter:
    """Export processed data and reports to output files."""

    def __init__(self, reports_dir: str, data_dir: str) -> None:
        self.reports_dir = Path(reports_dir)
        self.data_dir = Path(data_dir)
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def export_reports(self, reports: Dict[str, Any], records: Sequence[Dict[str, Any]]) -> None:
        write_json(str(self.reports_dir / "reports.json"), reports)
        write_json(str(self.data_dir / "processed_records.json"), list(records))
        write_csv(str(self.data_dir / "processed_records.csv"), list(records))
