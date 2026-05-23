# external_tool_layer.py

from typing import Dict, Any, Callable, Optional
import time
import uuid


class ExternalTool:
    """
    Wrapper for a callable external capability.
    """

    def __init__(self, name: str, fn: Callable, schema: Optional[Dict[str, Any]] = None):
        self.name = name
        self.fn = fn
        self.schema = schema or {}
        self.id = str(uuid.uuid4())


class ExternalToolLayer:
    """
    Controlled interface between RSIForge and external world.

    Responsibilities:
    - tool registration
    - permission gating
    - execution sandboxing
    - audit logging
    """

    def __init__(self, orchestrator, memory, identity_kernel):
        self.orchestrator = orchestrator
        self.memory = memory
        self.identity = identity_kernel

        self.tools: Dict[str, ExternalTool] = {}
        self.execution_log = []

    # -------------------------
    # Tool Registration
    # -------------------------
    def register_tool(self, name: str, fn: Callable, schema: Dict[str, Any] = None):
        tool = ExternalTool(name, fn, schema)
        self.tools[name] = tool

        self.orchestrator._log("tool_registered", {
            "tool": name,
            "id": tool.id
        })

    # -------------------------
    # Tool Validation Gate
    # -------------------------
    def validate_call(self, tool_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensures tool execution is allowed under identity + safety constraints.
        """

        if tool_name not in self.tools:
            return {"allowed": False, "reason": "unknown_tool"}

        # identity constraint hook
        if tool_name in getattr(self.identity, "invariants", set()):
            return {"allowed": False, "reason": "identity_invariant_violation"}

        # basic payload sanity check
        if payload is None:
            return {"allowed": False, "reason": "empty_payload"}

        return {"allowed": True}

    # -------------------------
    # Tool Execution
    # -------------------------
    def execute(self, tool_name: str, payload: Dict[str, Any], kernel_id: str = "global") -> Any:
        """
        Executes external tool safely.
        """

        decision = self.validate_call(tool_name, payload)

        if not decision["allowed"]:
            self.orchestrator._log("tool_execution_blocked", {
                "tool": tool_name,
                "reason": decision.get("reason")
            })
            return None

        tool = self.tools[tool_name]

        start = time.time()

        try:
            result = tool.fn(payload)

            success = True
            error = None

        except Exception as e:
            result = None
            success = False
            error = str(e)

        latency = time.time() - start

        log_entry = {
            "tool": tool_name,
            "payload": payload,
            "result": result,
            "success": success,
            "error": error,
            "latency": latency,
            "timestamp": time.time(),
            "kernel_id": kernel_id
        }

        self.execution_log.append(log_entry)

        # -------------------------
        # Persist into system memory
        # -------------------------
        self.memory.write_node(kernel_id, {
            "last_tool": tool_name,
            "last_tool_result": result,
            "tool_success": success
        })

        self.orchestrator._log("external_tool_executed", log_entry)

        return result

    # -------------------------
    # Tool Introspection
    # -------------------------
    def list_tools(self):
        return list(self.tools.keys())

    def get_tool(self, name: str) -> Optional[ExternalTool]:
        return self.tools.get(name)

    # -------------------------
    # Audit Layer
    # -------------------------
    def audit(self):
        """
        Reviews external system interactions for anomalies.
        """

        failures = [e for e in self.execution_log if not e["success"]]
        avg_latency = sum(e["latency"] for e in self.execution_log[-50:]) / max(1, len(self.execution_log[-50:]))

        report = {
            "failure_rate": len(failures) / max(1, len(self.execution_log)),
            "avg_latency": avg_latency,
            "total_calls": len(self.execution_log)
        }

        self.orchestrator._log("external_tool_audit", report)

        return report
