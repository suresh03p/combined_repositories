import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import unquote, urlsplit

from .runner import DurableAgentRunner
from .store import ExecutionNotFound, IdempotencyConflict


class ExecutionHTTPServer(ThreadingHTTPServer):
    daemon_threads = True


def make_handler(runner: DurableAgentRunner) -> type[BaseHTTPRequestHandler]:
    class ExecutionRequestHandler(BaseHTTPRequestHandler):
        server_version = "DurableAgentRunner/1.0"

        def do_GET(self) -> None:
            try:
                self._dispatch_get()
            except Exception as error:
                self._server_error(error)

        def _dispatch_get(self) -> None:
            path = urlsplit(self.path).path.rstrip("/") or "/"
            if path == "/health":
                self._send(200, {"status": "ok"})
                return
            if path == "/executions":
                self._send(200, {"executions": runner.list_executions()})
                return
            parts = [unquote(part) for part in path.split("/") if part]
            if len(parts) == 2 and parts[0] == "executions":
                self._get_execution(parts[1])
                return
            if len(parts) == 3 and parts[0] == "executions" and parts[2] == "history":
                try:
                    self._send(200, runner.get_history(parts[1]))
                except ExecutionNotFound:
                    self._send(404, {"error": "Execution not found."})
                return
            self._send(404, {"error": "Endpoint not found."})

        def _get_execution(self, task_id: str) -> None:
            try:
                self._send(200, runner.get_execution(task_id))
            except ExecutionNotFound:
                self._send(404, {"error": "Execution not found."})

        def do_POST(self) -> None:
            try:
                self._dispatch_post()
            except Exception as error:
                self._server_error(error)

        def _dispatch_post(self) -> None:
            path = urlsplit(self.path).path.rstrip("/")
            if path == "/executions":
                self._create_execution()
                return
            parts = [unquote(part) for part in path.split("/") if part]
            if len(parts) == 3 and parts[0] == "executions":
                self._change_execution(parts[1], parts[2])
                return
            self._send(404, {"error": "Endpoint not found."})

        def _create_execution(self) -> None:
            try:
                body = self._read_json()
                if not isinstance(body, dict):
                    raise ValueError("The JSON body must be an object.")
                input_text = body.get("input_text")
                if not isinstance(input_text, str) or not input_text.strip():
                    raise ValueError("input_text must be a non-empty string.")
                if len(input_text) > 10_000:
                    raise ValueError("input_text must be at most 10000 characters.")
                conversation_id = body.get("conversation_id")
                if conversation_id is not None and not isinstance(conversation_id, str):
                    raise ValueError("conversation_id must be a string.")
                key = self.headers.get("Idempotency-Key") or body.get("idempotency_key")
                if key is not None and (
                    not isinstance(key, str) or not key.strip() or len(key) > 200
                ):
                    raise ValueError("idempotency_key must be a non-empty string of at most 200 characters.")
                execution, created = runner.create_execution(
                    input_text, key, conversation_id
                )
                self._send(202 if created else 200, execution)
            except IdempotencyConflict as error:
                self._send(409, {"error": str(error)})
            except (ValueError, json.JSONDecodeError) as error:
                self._send(400, {"error": str(error)})

        def _change_execution(self, task_id: str, action: str) -> None:
            try:
                if action == "resume":
                    execution = runner.resume(task_id)
                elif action == "pause":
                    execution = runner.pause(task_id)
                elif action == "cancel":
                    execution = runner.cancel(task_id)
                else:
                    self._send(404, {"error": "Action not found."})
                    return
                self._send(202, execution)
            except ExecutionNotFound:
                self._send(404, {"error": "Execution not found."})
            except ValueError as error:
                self._send(409, {"error": str(error)})

        def _read_json(self) -> Any:
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError as error:
                raise ValueError("Content-Length must be an integer.") from error
            if length < 0 or length > 65_536:
                raise ValueError("Request body must be at most 65536 bytes.")
            raw = self.rfile.read(length)
            try:
                return json.loads(raw.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise ValueError("Request body must contain valid JSON.") from error

        def _send(self, status: int, payload: Any) -> None:
            encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def _server_error(self, error: Exception) -> None:
            self.log_error("Request failed for %s: %s", self.path, error)
            self._send(500, {"error": "Internal server error."})

        def log_message(self, format_string: str, *args: Any) -> None:
            print(f"{self.log_date_time_string()} {format_string % args}")

    return ExecutionRequestHandler


def create_server(
    runner: DurableAgentRunner, host: str = "127.0.0.1", port: int = 8000
) -> ExecutionHTTPServer:
    return ExecutionHTTPServer((host, port), make_handler(runner))
