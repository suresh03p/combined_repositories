"""Run the illustrative parallel multi-agent research demo."""

import asyncio
import json

from src.agents.demo_agents import build_demo_agents
from src.orchestration.supervisor import Supervisor


async def main() -> None:
    supervisor = Supervisor(build_demo_agents())
    state = await supervisor.run()
    print(json.dumps(state.to_dict(), indent=2, ensure_ascii=True))
    print(f"\nExecution trace: {supervisor.trace_path}")


if __name__ == "__main__":
    asyncio.run(main())