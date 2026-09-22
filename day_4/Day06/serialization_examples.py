"""Serialization examples using pickle, JSON, CSV, XML, and optional YAML."""

from __future__ import annotations

import csv
import json
import pickle
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None


class EmployeeDataSerializer:
    """Serialize employee records in multiple formats."""

    def __init__(self, employee: dict[str, object]) -> None:
        self.employee = employee

    def to_json(self, path: Path) -> None:
        path.write_text(json.dumps(self.employee, indent=2), encoding="utf-8")

    def to_pickle(self, path: Path) -> None:
        with path.open("wb") as handle:
            pickle.dump(self.employee, handle)

    def to_csv(self, path: Path) -> None:
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["name", "role", "salary"])
            writer.writeheader()
            writer.writerow(self.employee)

    def to_xml(self, path: Path) -> None:
        root = ET.Element("employee")
        for key, value in self.employee.items():
            child = ET.SubElement(root, key)
            child.text = str(value)
        ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)

    def to_yaml(self, path: Path) -> None:
        if yaml is None:
            raise ImportError("PyYAML is not installed")
        path.write_text(yaml.safe_dump(self.employee, sort_keys=False), encoding="utf-8")


class ConfigurationExporter:
    """Export configuration settings to JSON."""

    @staticmethod
    def export(path: Path, config: dict[str, object]) -> None:
        path.write_text(json.dumps(config, indent=2), encoding="utf-8")


class BackupUtility:
    """Create a zip archive of data files."""

    @staticmethod
    def backup(files: list[Path], archive_path: Path) -> None:
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for file_path in files:
                archive.write(file_path, arcname=file_path.name)


class RestoreUtility:
    """Restore archived files to a target folder."""

    @staticmethod
    def restore(archive_path: Path, destination: Path) -> None:
        with zipfile.ZipFile(archive_path, "r") as archive:
            archive.extractall(destination)


def demo(output_dir: Path | None = None) -> dict[str, object]:
    """Create sample serialized outputs."""
    output_dir = output_dir or Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)
    employee = {"name": "Ravi", "role": "Engineer", "salary": 75000}
    serializer = EmployeeDataSerializer(employee)
    serializer.to_json(output_dir / "employee.json")
    serializer.to_pickle(output_dir / "employee.pkl")
    serializer.to_csv(output_dir / "employee.csv")
    serializer.to_xml(output_dir / "employee.xml")
    try:
        serializer.to_yaml(output_dir / "employee.yaml")
    except ImportError:
        print("PyYAML is not installed; YAML export skipped")
    ConfigurationExporter.export(output_dir / "config.json", {"debug": True, "port": 8000})
    BackupUtility.backup([output_dir / "employee.json", output_dir / "config.json"], output_dir / "backup.zip")
    return {"output_dir": str(output_dir)}


if __name__ == "__main__":
    print(demo())
