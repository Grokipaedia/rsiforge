# forge_orchestrator.py

from dataclasses import dataclass, field
from typing import Dict, Any, List, Callable, Optional
import time
import json


@dataclass
class ForgeEvent:
    timestamp: float
    event_type: str
    payload: Dict[str, Any]


@dataclass
class ForgeState:
    memory: Dict[str, Any] = field(default_factory=dict)
    registry: Dict[str, Callable] = field(default_factory=dict)
    event_log: List[ForgeEvent] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


class ForgeOrchestrator:
    """
    Central execution + coordination layer for RSIForge.
    Handles:
    - module registration
    - event emission
    - state mutation
    - execution routing
    """

    def __init__(self, name: str = "rsiforge"):
        self.state = ForgeState(meta={"name": name, "created": time.time()})

    # -------------------------
    # Registry System
    # -------------------------
    def register(self, name: str, fn: Callable):
        """Register a callable module into the forge."""
        self.state.registry[name] = fn
        self._log("register", {"module": name})

    def unregister(self, name: str):
        """Remove module from registry."""
        if name in self.state.registry:
            del self.state.registry[name]
            self._log("unregister", {"module": name})

    # -------------------------
    # Execution Layer
    # -------------------------
    def run(self, module: str, input_data: Dict[str, Any]) -> Any:
        """Execute a registered module."""
        if module not in self.state.registry:
            raise ValueError(f"Module not found in forge: {module}")

        self._log("run_start", {"module": module, "input": input_data})

        result = self.state.registry[module](self.state, input_data)

        self._log("run_end", {"module": module, "output": result})

        return result

    # -------------------------
    # Memory Layer
    # -------------------------
    def write_memory(self, key: str, value: Any):
        self.state.memory[key] = value
        self._log("memory_write", {"key": key})

    def read_memory(self, key: str, default=None):
        return self.state.memory.get(key, default)

    # -------------------------
    # Event System
    # -------------------------
    def _log(self, event_type: str, payload: Dict[str, Any]):
        self.state.event_log.append(
            ForgeEvent(
                timestamp=time.time(),
                event_type=event_type,
                payload=payload
            )
        )

    def export_state(self) -> Dict[str, Any]:
        """Export full system state for persistence/debugging."""
        return {
            "memory": self.state.memory,
            "meta": self.state.meta,
            "events": [
                {
                    "t": e.timestamp,
                    "type": e.event_type,
                    "payload": e.payload
                }
                for e in self.state.event_log
            ],
            "registry": list(self.state.registry.keys())
        }

    def save(self, path: str):
        """Persist state to disk."""
        with open(path, "w") as f:
            json.dump(self.export_state(), f, indent=2)
