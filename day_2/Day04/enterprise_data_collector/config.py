import json
from pathlib import Path
from typing import Any, Dict, List


class Config:
    """Load configuration from a JSON file."""

    def __init__(self, config_path: str = "config/config.json") -> None:
        self.base_dir = Path(__file__).resolve().parent
        config_path_obj = Path(config_path)
        self.config_path = (
            (self.base_dir / config_path_obj).resolve()
            if not config_path_obj.is_absolute()
            else config_path_obj.resolve()
        )
        self._raw_config = self._load_config()
        self.api_endpoints: List[str] = self._raw_config.get("api_endpoints", [])
        self.request_timeout: int = int(self._raw_config.get("request_timeout", 5))
        self.max_retries: int = int(self._raw_config.get("max_retries", 3))
        self.retry_delay: float = float(self._raw_config.get("retry_delay", 0.5))
        self.log_level: str = str(self._raw_config.get("log_level", "INFO"))
        self.reports_dir: str = self._resolve_path(self._raw_config.get("reports_dir", "reports"))
        self.data_dir: str = self._resolve_path(self._raw_config.get("data_dir", "data"))

    def _resolve_path(self, value: str) -> str:
        path = Path(value)
        if not path.is_absolute():
            path = self.base_dir / path
        return str(path.resolve())

    def _load_config(self) -> Dict[str, Any]:
        with self.config_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
