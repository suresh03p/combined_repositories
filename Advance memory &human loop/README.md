# Secure Multi-Agent Workflow

A dependency-free Python demo of persistent memory, least-privilege tool access, human approval, prompt-injection boundaries, redaction, execution budgets, and JSON audit logging. All tools are local simulations: this project does not send messages, change external records, or contact external services.

## Run

From the workspace root:

```powershell
python -m secure_agent.demo
python -m unittest discover -s tests -v
```

The demo runs a scripted approval sequence and writes `outputs/audit_log.json`. To make each decision yourself in the terminal:

```powershell
python -m secure_agent.demo --interactive
```

The scripted run approves the message, record modification, and external-operation simulation, and rejects the delete. Running it again appends audit history.

## Memory Model

| Type | Lifetime and contents | Storage |
|---|---|---|
| Short-term | Recent redacted context for the active workflow | In memory; bounded to the latest 8 items |
| Long-term | Reusable preferences, project facts, research, and decisions | `memory/long_term.json` |
| Conversation | Conversation ID, user/agent messages, tool calls, and important context | `outputs/conversations.json` |
| Task | Temporary state for the current request; cleared at each request | In memory only |
| Tool | Redacted tool arguments and outcomes for later retrieval/audit | `memory/tool_memory.json` |

`MemorySystem.retrieve(question, conversation_id)` searches matching long-term entries, conversation context, and tool history before the workflow continues. Long-term categories are deliberately constrained to `user_preference`, `project_information`, `previous_research`, and `decision`.

## Safety Flow

```text
User request
  -> input validation and memory retrieval
  -> tool allowlist and argument schema
  -> agent permission check
  -> human approval for sensitive actions
  -> simulated tool execution
  -> output redaction and JSON audit record
```

Sensitive actions (`send_message`, `modify_record`, `delete_record`, `external_operation`) return `pending_approval` and do not execute until `resolve_approval(request_id, approved=...)` receives a decision. `read_record` is read-only. `Research Agent`, `Analyst`, and `Writer` have `READ`; `Admin Agent` has the explicit `READ`, `WRITE`, `DELETE`, and `EXECUTE` grants. `ADMIN` is also available as a policy override.

The user message is stored as untrusted data, not interpreted as policy. Tools are selected from a fixed allowlist, argument keys and values are validated, and writable record fields are constrained. Outputs, memory, and audit fields redact common credential formats and labeled `PRIVATE_DOCUMENT`, `PERSONAL_INFO`, and `SYSTEM_PROMPT` content.

The default budget is 4,000 estimated tokens, 15 tool calls, 10 iterations, 60 seconds, and a small estimated cost cap. Token and cost accounting are deliberately approximate stand-ins; production integrations should use provider-reported usage and enforce limits at the model/tool gateway.

Audit entries in `outputs/audit_log.json` include the requester, agent, tool, redacted arguments, result, UTC timestamp, and approval status (`pending`, `approved`, `rejected`, or `not_required`). Rejected permission or validation attempts are logged as `not_approved`.

## Production Caveats

This is an educational control-flow example, not a hardened agent runtime. Regex redaction is not a complete DLP solution; arbitrary personal data and private documents require classification and policy-aware handling. A real deployment should use authenticated approvers, durable/atomic storage, tamper-evident audit logs, per-agent budgets, isolation for untrusted tool execution, strict data-access scopes, and independent output validation. Prompt-injection resistance must be enforced at tool/data boundaries and cannot rely on prompt wording alone.
