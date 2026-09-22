"""Entry point for the enterprise log analytics application."""

from __future__ import annotations

from pathlib import Path

from parser import LogParser
from validator import LogValidator
from analyzer import LogAnalyzer
from security import SecurityMonitor
from archive import ArchiveManager
from serializer import DataSerializer
from reports import ReportGenerator
from logger import get_logger


def main() -> None:
    logger = get_logger("app")
    base_dir = Path(__file__).resolve().parent
    log_files = [base_dir / "logs" / "sample.txt", base_dir / "logs" / "sample.csv", base_dir / "logs" / "sample.json"]

    parser = LogParser(base_dir / "logs")
    validator = LogValidator()
    analyzer = LogAnalyzer()
    security = SecurityMonitor()
    archive = ArchiveManager(base_dir / "archive")
    serializer = DataSerializer(base_dir / "reports")
    reports = ReportGenerator(base_dir / "reports")

    records = []
    for file_path in log_files:
        if file_path.exists():
            records.extend(parser.parse(file_path))

    valid_records = [record for record in records if validator.is_valid(record)]
    incidents = security.detect(valid_records)
    analyzer.ingest(valid_records)

    logger.info("Processed %s records", len(valid_records))
    reports.write_hourly_report(analyzer.hourly_summary())
    reports.write_daily_summary(analyzer.daily_summary())
    reports.write_top_errors(analyzer.top_errors())
    reports.write_user_activity(analyzer.user_activity())
    reports.write_security_incidents(incidents)

    archive.compress_logs(log_files)
    serializer.save_pickle(valid_records, base_dir / "archive" / "records.pkl")
    serializer.save_json(valid_records, base_dir / "archive" / "records.json")
    logger.info("Analytics completed")


if __name__ == "__main__":
    main()
