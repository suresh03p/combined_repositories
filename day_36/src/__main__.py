"""Run the demo pipeline from the command line."""

from __future__ import annotations

import argparse
import json

from src.supervisor import Supervisor


def main() -> None:
    parser = argparse.ArgumentParser(description="Run an enterprise research pipeline")
    parser.add_argument(
        "question",
        nargs="?",
        default="How did customer retention and revenue change in 2025, and what trends explain it?",
    )
    arguments = parser.parse_args()
    print(json.dumps(Supervisor().run(arguments.question), indent=2))


if __name__ == "__main__":
    main()