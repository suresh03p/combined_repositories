import argparse
import json
from pathlib import Path
from uuid import uuid4

from src.agents.supervisor import SupervisorAgent
from src.orchestration.state import AgentState


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="Run the offline multi-agent research workflow.")
    parser.add_argument(
        "--question",
        default="How can a supervisor coordinate specialized agents using shared state?",
        help="Research question for the workflow.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project_root / "outputs" / "multi_agent_state.json",
        help="Path for the final shared-state JSON.",
    )
    args = parser.parse_args()

    state = AgentState(conversation_id=str(uuid4()), user_request=args.question)
    supervisor = SupervisorAgent()
    state = supervisor.run(state)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(state.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    for handoff in supervisor.handoffs:
        if handoff["to"] == "supervisor":
            print(f"{handoff['from']} -> supervisor: {handoff['result_received']}")
        else:
            print(f"supervisor -> {handoff['to']}: {handoff['decision']}")
    print(f"\n{state.final_response}")
    print(f"\nState written to {args.output}")

    if state.task_status != "completed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
