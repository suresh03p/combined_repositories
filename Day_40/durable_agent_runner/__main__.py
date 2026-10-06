import argparse
from pathlib import Path

from .api import create_server
from .runner import DurableAgentRunner
from .store import ExecutionStore


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Run the durable agent execution API.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument(
        "--database",
        type=Path,
        default=project_root / "outputs" / "executions.sqlite3",
    )
    parser.add_argument(
        "--history-dir",
        type=Path,
        default=project_root / "outputs" / "execution_history",
    )
    args = parser.parse_args()

    store = ExecutionStore(args.database, args.history_dir)
    runner = DurableAgentRunner(store)
    server = create_server(runner, args.host, args.port)
    print(f"Durable Agent Runner listening on http://{args.host}:{args.port}")
    print(f"SQLite state: {args.database}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Durable Agent Runner.")
    finally:
        server.server_close()
        runner.close()


if __name__ == "__main__":
    main()
