import asyncio
import time
from pathlib import Path

from config import Config
from exporter import ReportExporter
from logger import setup_logger
from processor import DataProcessor
from utils import ensure_directory


async def main() -> None:
    """Run the enterprise data collector workflow."""
    config = Config(str(Path(__file__).resolve().parent / "config" / "config.json"))
    logger = setup_logger(config.log_level)
    ensure_directory(config.reports_dir)
    ensure_directory(config.data_dir)

    start_time = time.perf_counter()
    payloads = await collect_data(
        config.api_endpoints,
        timeout=config.request_timeout,
        max_retries=config.max_retries,
        retry_delay=config.retry_delay,
    )

    processor = DataProcessor()
    records = processor.process_payloads(payloads)
    reports = {
        "api_response_time_report": {"collected_endpoints": len(config.api_endpoints), "successful_endpoints": len(payloads)},
        "success_vs_failure_report": {"success_count": len(payloads), "failure_count": len(config.api_endpoints) - len(payloads)},
        "data_volume_report": {"processed_record_count": len(records), "aggregate": processor.aggregate(records)},
        "processing_time_report": {"processing_seconds": round(time.perf_counter() - start_time, 3)},
    }

    exporter = ReportExporter(config.reports_dir, config.data_dir)
    exporter.export_reports(reports, records)
    logger.info("Reports generated successfully")
    processor.shutdown()


if __name__ == "__main__":
    import sys

    sys.path.append(str(Path(__file__).resolve().parent))
    from async_tasks import collect_data

    asyncio.run(main())
