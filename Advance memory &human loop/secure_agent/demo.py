from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from .core import SecureAgentWorkflow, redact_sensitive


DEMO_ACTIONS: list[tuple[str, str, dict[str, str], bool]] = [
    (
        "send_message",
        "Send the rollout message to the team.",
        {"recipient": "team@example.test", "message": "The rollout is ready."},
        True,
    ),
    (
        "modify_record",
        "Update the demo record status.",
        {"record_id": "record-1", "field": "status", "value": "ready"},
        True,
    ),
    (
        "delete_record",
        "Delete the demo record.",
        {"record_id": "record-1"},
        False,
    ),
    (
        "external_operation",
        "Queue the demo synchronization operation.",
        {"operation": "sync-demo", "payload": "record-1"},
        True,
    ),
]


def _approval_decision(interactive: bool, default: bool, tool: str, arguments: dict[str, Any]) -> bool:
    if not interactive:
        return default
    print(f"\nApproval requested for {tool}: {redact_sensitive(arguments)}")
    return input("Approve? [y/N] ").strip().lower() in {"y", "yes"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the local secure-agent workflow demo.")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Ask for a human decision for every sensitive action.",
    )
    args = parser.parse_args()

    workflow = SecureAgentWorkflow(Path.cwd())
    if not workflow.memory.long_term.search("human confirmation external communication"):
        workflow.memory.long_term.add(
            "user_preference",
            "Require human confirmation before external communication.",
            ["approval", "message"],
        )

    conversation_id = workflow.memory.conversation.ensure()
    print("Secure multi-agent workflow (simulated tools; no external actions are sent).")
    for tool, request, arguments, default_decision in DEMO_ACTIONS:
        conversation_id, result, memories = workflow.handle_request(
            agent="Admin Agent",
            conversation_id=conversation_id,
            user_message=request,
            tool=tool,
            arguments=arguments,
            requested_by="demo-user",
        )
        if result.status == "pending_approval":
            approved = _approval_decision(args.interactive, default_decision, tool, arguments)
            result = workflow.resolve_approval(result.approval_request_id, approved=approved)
            workflow.memory.conversation.add_message(
                conversation_id,
                "agent",
                f"Human decision: {result.status}.",
            )
        print(f"{tool}: {result.status}" + (f" ({result.error})" if result.error else ""))
        if memories["long_term"]:
            print(f"  Retrieved reusable preference: {memories['long_term'][0]['text']}")

    print(f"Audit log: {workflow.audit_path}")
    print(f"Audit entries: {len(workflow.audit_entries)}")


if __name__ == "__main__":
    main()
