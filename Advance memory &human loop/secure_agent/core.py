from __future__ import annotations

import json
import re
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable


class Permission(str, Enum):
    READ = "READ"
    WRITE = "WRITE"
    DELETE = "DELETE"
    EXECUTE = "EXECUTE"
    ADMIN = "ADMIN"


class SecurityError(Exception):
    pass


class BudgetExceeded(SecurityError):
    pass


class PermissionDenied(SecurityError):
    pass


class InputRejected(SecurityError):
    pass


_SECRET_PATTERNS = (
    re.compile(r"(?i)\b(api[_ -]?key|password|token|secret)\s*[:=]\s*[^\s,;]+"),
    re.compile(r"\b(?:sk|pk)-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+"),
    re.compile(r"(?i)(?:PRIVATE_DOCUMENT|SYSTEM_PROMPT|PERSONAL_INFO)\s*:\s*.+"),
)
_SENSITIVE_KEY = re.compile(
    r"(?i)(?:api[_-]?key|password|token|secret|private[_-]?document|personal[_-]?info|system[_-]?prompt)"
)


def redact_sensitive(value: Any) -> Any:
    """Redact common secrets and explicitly classified private content recursively."""
    if isinstance(value, str):
        result = value
        for pattern in _SECRET_PATTERNS:
            result = pattern.sub("[REDACTED]", result)
        return result
    if isinstance(value, dict):
        return {
            str(key): "[REDACTED]" if _SENSITIVE_KEY.search(str(key)) else redact_sensitive(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact_sensitive(item) for item in value]
    if isinstance(value, tuple):
        return [redact_sensitive(item) for item in value]
    return value


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_user_input(message: str, max_length: int = 4000) -> str:
    if not isinstance(message, str) or not message.strip():
        raise InputRejected("User message must be a non-empty string.")
    if len(message) > max_length:
        raise InputRejected(f"User message exceeds {max_length} characters.")
    if any(ord(char) < 32 and char not in "\n\r\t" for char in message):
        raise InputRejected("User message contains unsupported control characters.")
    # The content remains data; it is never evaluated as policy or tool instructions.
    return message.strip()


@dataclass
class ShortTermMemory:
    max_items: int = 8
    items: list[str] = field(default_factory=list)

    def add(self, text: str) -> None:
        self.items.append(str(redact_sensitive(text)))
        self.items = self.items[-self.max_items :]


@dataclass
class TaskMemory:
    """Ephemeral state for one run; intentionally not persisted."""
    values: dict[str, Any] = field(default_factory=dict)


class ConversationMemory:
    def __init__(self, path: Path):
        self.path = path
        self.conversations: dict[str, dict[str, Any]] = _read_json(path, {})

    def ensure(self, conversation_id: str | None = None) -> str:
        conversation_id = conversation_id or str(uuid.uuid4())
        self.conversations.setdefault(
            conversation_id,
            {"messages": [], "tool_calls": [], "important_context": []},
        )
        return conversation_id

    def add_message(self, conversation_id: str, speaker: str, content: str) -> None:
        conversation = self.conversations[conversation_id]
        conversation["messages"].append(
            {"speaker": speaker, "content": redact_sensitive(content), "timestamp": _timestamp()}
        )
        _write_json(self.path, self.conversations)

    def add_tool_call(self, conversation_id: str, call: dict[str, Any]) -> None:
        self.conversations[conversation_id]["tool_calls"].append(redact_sensitive(call))
        _write_json(self.path, self.conversations)

    def add_important_context(self, conversation_id: str, context: str) -> None:
        self.conversations[conversation_id]["important_context"].append(
            str(redact_sensitive(context))
        )
        _write_json(self.path, self.conversations)

    def search(self, conversation_id: str, query: str) -> list[str]:
        conversation = self.conversations.get(conversation_id, {})
        terms = {term.lower() for term in re.findall(r"[\w-]+", query) if len(term) > 2}
        candidates = [
            str(message["content"])
            for message in conversation.get("messages", [])
            if message.get("speaker") == "user"
        ] + list(conversation.get("important_context", []))
        ranked = sorted(
            ((sum(term in text.lower() for term in terms), text) for text in candidates),
            key=lambda item: item[0],
            reverse=True,
        )
        return [text for score, text in ranked if score > 0][:5]


class LongTermKnowledgeMemory:
    CATEGORIES = {"user_preference", "project_information", "previous_research", "decision"}

    def __init__(self, path: Path):
        self.path = path
        self.entries: list[dict[str, Any]] = _read_json(path, [])

    def add(self, category: str, text: str, tags: list[str] | None = None) -> str:
        if category not in self.CATEGORIES:
            raise InputRejected(f"Unsupported knowledge category: {category}")
        if not isinstance(text, str) or not text.strip():
            raise InputRejected("Knowledge text must not be empty.")
        entry_id = str(uuid.uuid4())
        self.entries.append(
            {
                "id": entry_id,
                "category": category,
                "text": redact_sensitive(text.strip()),
                "tags": redact_sensitive(tags or []),
                "created_at": _timestamp(),
            }
        )
        _write_json(self.path, self.entries)
        return entry_id

    def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        terms = {term.lower() for term in re.findall(r"[\w-]+", query) if len(term) > 2}
        ranked = []
        for entry in self.entries:
            searchable = " ".join([entry["text"], *entry.get("tags", []), entry["category"]]).lower()
            score = sum(term in searchable for term in terms)
            if score:
                ranked.append((score, entry))
        ranked.sort(key=lambda item: (-item[0], item[1]["created_at"]))
        return [dict(entry) for _, entry in ranked[:limit]]


class ToolMemory:
    def __init__(self, path: Path):
        self.path = path
        self.entries: list[dict[str, Any]] = _read_json(path, [])

    def record(self, entry: dict[str, Any]) -> None:
        self.entries.append(redact_sensitive(entry))
        _write_json(self.path, self.entries)

    def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        terms = {term.lower() for term in re.findall(r"[\w-]+", query) if len(term) > 2}
        ranked = []
        for entry in self.entries:
            searchable = json.dumps(entry, ensure_ascii=True).lower()
            score = sum(term in searchable for term in terms)
            if score:
                ranked.append((score, entry))
        ranked.sort(key=lambda item: (-item[0], item[1]["timestamp"]))
        return [dict(entry) for _, entry in ranked[:limit]]


class MemorySystem:
    def __init__(self, root: Path):
        self.short_term = ShortTermMemory()
        self.task = TaskMemory()
        self.conversation = ConversationMemory(root / "outputs" / "conversations.json")
        self.long_term = LongTermKnowledgeMemory(root / "memory" / "long_term.json")
        self.tool = ToolMemory(root / "memory" / "tool_memory.json")

    def retrieve(self, question: str, conversation_id: str) -> dict[str, list[Any]]:
        return {
            "long_term": self.long_term.search(question),
            "conversation": self.conversation.search(conversation_id, question),
            "tool": self.tool.search(question),
            "short_term": self.short_term.items[-3:],
        }


@dataclass(frozen=True)
class AgentPolicy:
    name: str
    permissions: frozenset[Permission]

    def allows(self, permission: Permission) -> bool:
        return Permission.ADMIN in self.permissions or permission in self.permissions


DEFAULT_POLICIES = {
    "Research Agent": AgentPolicy("Research Agent", frozenset({Permission.READ})),
    "Analyst": AgentPolicy("Analyst", frozenset({Permission.READ})),
    "Writer": AgentPolicy("Writer", frozenset({Permission.READ})),
    "Admin Agent": AgentPolicy(
        "Admin Agent",
        frozenset({Permission.READ, Permission.WRITE, Permission.DELETE, Permission.EXECUTE}),
    ),
}


@dataclass
class AgentBudget:
    max_tokens: int = 4000
    max_tool_calls: int = 15
    max_iterations: int = 10
    max_execution_seconds: float = 60.0
    max_cost: float = 0.05
    tokens_used: int = 0
    tool_calls: int = 0
    iterations: int = 0
    cost_used: float = 0.0
    started_at: float = field(default_factory=time.monotonic)

    def consume(self, text: str = "", *, tool_call: bool = False) -> None:
        self.iterations += 1
        self.tokens_used += max(1, (len(text) + 3) // 4) if text else 0
        if tool_call:
            self.tool_calls += 1
        self.cost_used = self.tokens_used * 0.000002
        if self.tokens_used > self.max_tokens:
            raise BudgetExceeded("Maximum token budget exceeded.")
        if self.tool_calls > self.max_tool_calls:
            raise BudgetExceeded("Maximum tool-call budget exceeded.")
        if self.iterations > self.max_iterations:
            raise BudgetExceeded("Maximum iteration budget exceeded.")
        if time.monotonic() - self.started_at > self.max_execution_seconds:
            raise BudgetExceeded("Maximum execution time exceeded.")
        if self.cost_used > self.max_cost:
            raise BudgetExceeded("Maximum cost budget exceeded.")


@dataclass
class ApprovalRequest:
    request_id: str
    requested_by: str
    agent: str
    tool: str
    arguments: dict[str, Any]
    created_at: str
    status: str = "pending"


@dataclass
class ActionResult:
    status: str
    result: Any = None
    approval_request_id: str | None = None
    error: str | None = None


class SecureAgentWorkflow:
    """A local, deterministic secure-agent workflow. All tool effects are simulated."""

    TOOL_PERMISSIONS = {
        "send_message": Permission.WRITE,
        "modify_record": Permission.WRITE,
        "delete_record": Permission.DELETE,
        "external_operation": Permission.EXECUTE,
        "read_record": Permission.READ,
    }
    APPROVAL_REQUIRED = {"send_message", "modify_record", "delete_record", "external_operation"}

    def __init__(
        self,
        root: Path,
        *,
        policies: dict[str, AgentPolicy] | None = None,
        records: dict[str, dict[str, Any]] | None = None,
        budget: AgentBudget | None = None,
    ):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.audit_path = self.root / "outputs" / "audit_log.json"
        self.audit_entries: list[dict[str, Any]] = _read_json(self.audit_path, [])
        self.memory = MemorySystem(self.root)
        self.policies = policies or DEFAULT_POLICIES
        self.records = records if records is not None else {"record-1": {"status": "draft"}}
        self.outbox: list[str] = []
        self.external_operations: list[dict[str, Any]] = []
        self.pending_approvals: dict[str, ApprovalRequest] = {}
        self.budget = budget or AgentBudget()
        self.requested_by = "local-user"

    def _audit(
        self,
        *,
        agent: str,
        tool: str,
        arguments: dict[str, Any],
        result: Any,
        approval_status: str,
        requested_by: str | None = None,
    ) -> None:
        entry = redact_sensitive(
            {
                "timestamp": _timestamp(),
                "requested_by": requested_by or self.requested_by,
                "agent": agent,
                "tool": tool,
                "arguments": arguments,
                "result": result,
                "approval_status": approval_status,
            }
        )
        self.audit_entries.append(entry)
        _write_json(self.audit_path, self.audit_entries)
        self.memory.tool.record(entry)

    def _validate_arguments(self, tool: str, arguments: dict[str, Any]) -> dict[str, str]:
        schemas = {
            "send_message": {"recipient", "message"},
            "modify_record": {"record_id", "field", "value"},
            "delete_record": {"record_id"},
            "external_operation": {"operation", "payload"},
            "read_record": {"record_id"},
        }
        if tool not in schemas:
            raise InputRejected("Tool is not in the allowlist.")
        if not isinstance(arguments, dict) or set(arguments) != schemas[tool]:
            raise InputRejected(f"Invalid arguments for tool {tool}.")
        if any(not isinstance(value, str) or len(value) > 1000 for value in arguments.values()):
            raise InputRejected("Tool arguments must be strings of at most 1000 characters.")
        if any(not value.strip() for value in arguments.values()):
            raise InputRejected("Tool arguments must not be empty.")
        if tool == "modify_record" and arguments["field"] not in {"status", "owner", "notes"}:
            raise InputRejected("Record field is not in the writable allowlist.")
        return arguments

    def _run_tool(self, tool: str, arguments: dict[str, str]) -> Any:
        if tool == "send_message":
            self.outbox.append(f"To: {arguments['recipient']} | {arguments['message']}")
            return {"sent": True, "recipient": arguments["recipient"]}
        if tool == "modify_record":
            record = self.records.get(arguments["record_id"])
            if record is None:
                raise InputRejected("Record does not exist.")
            record[arguments["field"]] = arguments["value"]
            return {"updated": arguments["record_id"], "field": arguments["field"]}
        if tool == "delete_record":
            if arguments["record_id"] not in self.records:
                raise InputRejected("Record does not exist.")
            del self.records[arguments["record_id"]]
            return {"deleted": arguments["record_id"]}
        if tool == "external_operation":
            operation = {"operation": arguments["operation"], "payload": arguments["payload"]}
            self.external_operations.append(operation)
            return {"queued": True, "operation": arguments["operation"]}
        if tool == "read_record":
            record = self.records.get(arguments["record_id"])
            if record is None:
                raise InputRejected("Record does not exist.")
            return record
        raise InputRejected("Tool is not in the allowlist.")

    def call_tool(
        self,
        *,
        agent: str,
        requested_by: str,
        conversation_id: str,
        tool: str,
        arguments: dict[str, Any],
        approval: bool | None = None,
    ) -> ActionResult:
        self.requested_by = requested_by
        try:
            self.budget.consume(json.dumps(arguments, ensure_ascii=True), tool_call=True)
            if tool not in self.TOOL_PERMISSIONS:
                raise InputRejected("Tool is not in the allowlist.")
            policy = self.policies.get(agent)
            if policy is None or not policy.allows(self.TOOL_PERMISSIONS[tool]):
                raise PermissionDenied(f"Agent {agent!r} is not permitted to call {tool!r}.")
            safe_arguments = self._validate_arguments(tool, arguments)
        except (SecurityError, TypeError, ValueError) as error:
            self._audit(
                agent=agent,
                tool=tool,
                arguments=arguments if isinstance(arguments, dict) else {"invalid": str(arguments)},
                result={"error": str(error)},
                approval_status="not_approved",
            )
            return ActionResult("rejected", error=str(error))

        self.memory.conversation.add_tool_call(
            conversation_id,
            {"tool": tool, "arguments": safe_arguments, "timestamp": _timestamp()},
        )
        if tool in self.APPROVAL_REQUIRED:
            request = ApprovalRequest(
                request_id=str(uuid.uuid4()),
                requested_by=requested_by,
                agent=agent,
                tool=tool,
                arguments=safe_arguments,
                created_at=_timestamp(),
            )
            self.pending_approvals[request.request_id] = request
            if approval is None:
                self._audit(
                    agent=agent,
                    tool=tool,
                    arguments=safe_arguments,
                    result={"approval_request_id": request.request_id},
                    approval_status="pending",
                    requested_by=requested_by,
                )
                return ActionResult("pending_approval", approval_request_id=request.request_id)
            return self.resolve_approval(request.request_id, approved=approval)

        try:
            result = redact_sensitive(self._run_tool(tool, safe_arguments))
            status = "not_required"
            response = ActionResult("completed", result=result)
        except (InputRejected, KeyError) as error:
            result = {"error": str(error)}
            status = "not_approved"
            response = ActionResult("rejected", error=str(error))
        self._audit(
            agent=agent,
            tool=tool,
            arguments=safe_arguments,
            result=result,
            approval_status=status,
            requested_by=requested_by,
        )
        return response

    def resolve_approval(self, request_id: str, *, approved: bool) -> ActionResult:
        request = self.pending_approvals.get(request_id)
        if request is None or request.status != "pending":
            return ActionResult("rejected", error="Approval request is missing or already resolved.")
        request.status = "approved" if approved else "rejected"
        if not approved:
            result = {"error": "Human rejected the action."}
            self._audit(
                agent=request.agent,
                tool=request.tool,
                arguments=request.arguments,
                result=result,
                approval_status="rejected",
                requested_by=request.requested_by,
            )
            return ActionResult("rejected", error="Human rejected the action.")
        try:
            result = redact_sensitive(self._run_tool(request.tool, request.arguments))
            response = ActionResult("completed", result=result)
        except (InputRejected, KeyError) as error:
            result = {"error": str(error)}
            response = ActionResult("rejected", error=str(error))
        self._audit(
            agent=request.agent,
            tool=request.tool,
            arguments=request.arguments,
            result=result,
            approval_status="approved",
            requested_by=request.requested_by,
        )
        return response

    def handle_request(
        self,
        *,
        agent: str,
        conversation_id: str | None,
        user_message: str,
        tool: str,
        arguments: dict[str, Any],
        approval: bool | None = None,
        requested_by: str = "local-user",
    ) -> tuple[str, ActionResult, dict[str, list[Any]]]:
        message = validate_user_input(user_message)
        conversation_id = self.memory.conversation.ensure(conversation_id)
        self.budget.consume(message)
        self.memory.task.values.clear()
        self.memory.conversation.add_message(conversation_id, "user", message)
        self.memory.short_term.add(message)
        self.memory.task.values["last_request"] = message
        retrieved = self.memory.retrieve(message, conversation_id)
        result = self.call_tool(
            agent=agent,
            requested_by=requested_by,
            conversation_id=conversation_id,
            tool=tool,
            arguments=arguments,
            approval=approval,
        )
        response_text = (
            f"Action {result.status}: {result.error or result.result or result.approval_request_id}"
        )
        self.memory.conversation.add_message(conversation_id, "agent", response_text)
        self.memory.short_term.add(response_text)
        return conversation_id, result, retrieved
