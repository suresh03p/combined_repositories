"""Validation and construction for versioned agent-to-agent handoffs."""

from typing import Any


SCHEMA_VERSION = "1.0"
STEP_ROLES = {
    "plan": ("planner", "researcher"),
    "research": ("researcher", "validator"),
    "respond": ("validator", "terminal"),
}


class HandoffValidationError(ValueError):
    """A handoff does not satisfy the role boundary contract."""


class AgentHandoffError(RuntimeError):
    """An agent reported an expected, structured failure."""


def make_handoff(
    step: str,
    task_id: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    try:
        from_role, to_role = STEP_ROLES[step]
    except KeyError as error:
        raise HandoffValidationError(f"Unknown workflow step: {step}.") from error
    handoff = {
        "schema_version": SCHEMA_VERSION,
        "from_role": from_role,
        "to_role": to_role,
        "task_id": task_id,
        "status": "completed",
        "payload": payload,
    }
    validate_handoff(handoff, step, task_id)
    return handoff


def validate_handoff(
    handoff: Any,
    step: str,
    task_id: str,
) -> dict[str, Any]:
    if not isinstance(handoff, dict):
        raise HandoffValidationError("Handoff must be a JSON object.")
    try:
        expected_from, expected_to = STEP_ROLES[step]
    except KeyError as error:
        raise HandoffValidationError(f"Unknown workflow step: {step}.") from error

    required = {
        "schema_version",
        "from_role",
        "to_role",
        "task_id",
        "status",
    }
    status = handoff.get("status")
    if status == "completed":
        required.add("payload")
    elif status == "error":
        required.add("error")
    else:
        raise HandoffValidationError("status must be 'completed' or 'error'.")
    if set(handoff) != required:
        raise HandoffValidationError(
            f"Handoff fields must be exactly: {', '.join(sorted(required))}."
        )
    if handoff["schema_version"] != SCHEMA_VERSION:
        raise HandoffValidationError(
            f"schema_version must be '{SCHEMA_VERSION}'."
        )
    if handoff["from_role"] != expected_from:
        raise HandoffValidationError(f"from_role must be '{expected_from}'.")
    if handoff["to_role"] != expected_to:
        raise HandoffValidationError(f"to_role must be '{expected_to}'.")
    if handoff["task_id"] != task_id:
        raise HandoffValidationError("task_id does not match the active execution.")

    if status == "error":
        error = handoff["error"]
        if (
            not isinstance(error, dict)
            or set(error) != {"code", "message"}
            or not _non_empty_string(error.get("code"))
            or not _non_empty_string(error.get("message"))
        ):
            raise HandoffValidationError(
                "error must contain non-empty code and message strings."
            )
        raise AgentHandoffError(f"{error['code']}: {error['message']}")

    payload = handoff["payload"]
    _validate_payload(step, payload)
    return payload


def _validate_payload(step: str, payload: Any) -> None:
    if not isinstance(payload, dict):
        raise HandoffValidationError("payload must be a JSON object.")

    if step == "plan":
        if set(payload) != {"goal", "research_questions"}:
            raise HandoffValidationError(
                "planner payload must contain only goal and research_questions."
            )
        if not _non_empty_string(payload["goal"]):
            raise HandoffValidationError("planner goal must be a non-empty string.")
        questions = payload["research_questions"]
        if (
            not isinstance(questions, list)
            or not questions
            or not all(_non_empty_string(question) for question in questions)
        ):
            raise HandoffValidationError(
                "research_questions must be a non-empty array of non-empty strings."
            )
        return

    if step == "research":
        if set(payload) != {"findings", "limitations"}:
            raise HandoffValidationError(
                "researcher payload must contain only findings and limitations."
            )
        findings = payload["findings"]
        if (
            not isinstance(findings, list)
            or not findings
            or not all(
                isinstance(finding, dict)
                and set(finding) == {"claim", "evidence"}
                and _non_empty_string(finding["claim"])
                and _non_empty_string(finding["evidence"])
                for finding in findings
            )
        ):
            raise HandoffValidationError(
                "findings must be a non-empty array of claim/evidence objects."
            )
        limitations = payload["limitations"]
        if not isinstance(limitations, list) or not all(
            _non_empty_string(limitation) for limitation in limitations
        ):
            raise HandoffValidationError(
                "limitations must be an array of non-empty strings."
            )
        return

    if step == "respond":
        if set(payload) != {"accepted", "answer", "issues"}:
            raise HandoffValidationError(
                "validator payload must contain only accepted, answer, and issues."
            )
        if not isinstance(payload["accepted"], bool):
            raise HandoffValidationError("validator accepted must be a boolean.")
        if not _non_empty_string(payload["answer"]):
            raise HandoffValidationError("validator answer must be a non-empty string.")
        issues = payload["issues"]
        if not isinstance(issues, list) or not all(
            _non_empty_string(issue) for issue in issues
        ):
            raise HandoffValidationError("validator issues must be an array of strings.")


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())
