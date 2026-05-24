# rsiforge_observability_telemetry_layer.py

from typing import Dict, Any, List
import time
import uuid


class TelemetryEvent:
    """
    Represents a single traceable system event.
    """

    def __init__(self, event_type: str, payload: Dict[str, Any]):
        self.id = str(uuid.uuid4())
        self.event_type = event_type
        self.payload = payload
        self.timestamp = time.time()


class RSIForgeObservabilityTelemetryLayer:
    """
    Full-system observability, tracing, and runtime introspection layer.

    This layer does NOT modify cognition.
    It only observes, records, and reconstructs system behavior.
    """

    def __init__(self):
        self.event_log: List[TelemetryEvent] = []
        self.execution_traces: Dict[str, List[TelemetryEvent]] = {}

        self.system_health = {
            "loop_stability": 1.0,
            "mutation_rate": 0.0,
            "evaluation_drift": 0.0,
            "runtime_errors": 0
        }

    # -------------------------
    # Step 1: Log system event
    # -------------------------
    def log_event(self, event_type: str, payload: Dict[str, Any]):
        """
        Captures all system-level actions.
        """

        event = TelemetryEvent(event_type, payload)
        self.event_log.append(event)

        trace_id = payload.get("trace_id")

        if trace_id:
            if trace_id not in self.execution_traces:
                self.execution_traces[trace_id] = []

            self.execution_traces[trace_id].append(event)

    # -------------------------
    # Step 2: Monitor system health
    # -------------------------
    def update_health_metrics(self):
        """
        Aggregates runtime signals into system health indicators.
        """

        mutation_events = sum(
            1 for e in self.event_log if e.event_type == "mutation"
        )

        evaluation_events = sum(
            1 for e in self.event_log if e.event_type == "evaluation"
        )

        error_events = sum(
            1 for e in self.event_log if e.event_type == "error"
        )

        total = max(len(self.event_log), 1)

        self.system_health["mutation_rate"] = mutation_events / total
        self.system_health["evaluation_drift"] = abs(mutation_events - evaluation_events) / total
        self.system_health["runtime_errors"] = error_events

    # -------------------------
    # Step 3: Replay execution trace
    # -------------------------
    def replay_trace(self, trace_id: str) -> List[Dict[str, Any]]:
        """
        Reconstructs full decision chain for a system execution.
        """

        trace = self.execution_traces.get(trace_id, [])

        return [
            {
                "event_type": e.event_type,
                "payload": e.payload,
                "timestamp": e.timestamp
            }
            for e in trace
        ]

    # -------------------------
    # Step 4: Detect instability
    # -------------------------
    def detect_instability(self) -> Dict[str, Any]:
        """
        Identifies system-level instability patterns.
        """

        instability_score = (
            self.system_health["mutation_rate"] * 0.5 +
            self.system_health["evaluation_drift"] * 0.3 +
            (self.system_health["runtime_errors"] * 0.2)
        )

        return {
            "instability_score": instability_score,
            "safe": instability_score < 0.7
        }

    # -------------------------
    # Step 5: Export system snapshot
    # -------------------------
    def export_snapshot(self) -> Dict[str, Any]:
        """
        Produces full system state snapshot for debugging or replay.
        """

        return {
            "event_count": len(self.event_log),
            "health": self.system_health,
            "trace_count": len(self.execution_traces)
        }
