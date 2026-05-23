# goal_emergence_engine.py

from typing import Dict, Any, List
import time
import uuid


class GoalEmergenceEngine:
    """
    Generates new goals from internal system state.

    This is what transforms RSIForge from:
    reactive system → autonomous system.
    """

    def __init__(self, orchestrator, memory_graph, attention_router):
        self.orchestrator = orchestrator
        self.memory = memory_graph
        self.attention = attention_router

    # -------------------------
    # Main Emergence Cycle
    # -------------------------
    def generate_goals(self) -> List[Dict[str, Any]]:
        """
        Produces new goals based on system pressure signals.
        """

        goals = []

        # 1. memory pressure signals
        goals.extend(self._from_memory_clusters())

        # 2. attention hotspots
        goals.extend(self._from_attention_hotspots())

        # 3. unresolved execution patterns
        goals.extend(self._from_failure_patterns())

        self.orchestrator._log("goal_emergence_cycle", {
            "generated": len(goals)
        })

        return goals

    # -------------------------
    # Memory-driven goal generation
    # -------------------------
    def _from_memory_clusters(self) -> List[Dict[str, Any]]:
        clusters = {}

        for node_id, node in self.memory.nodes.items():
            for tag in node.tags:
                clusters.setdefault(tag, 0)
                clusters[tag] += 1

        goals = []

        for tag, strength in clusters.items():
            if strength > 3:
                goals.append({
                    "id": str(uuid.uuid4()),
                    "type": "analyze",
                    "priority": strength,
                    "payload": {
                        "tags": [tag],
                        "source": "memory_cluster"
                    }
                })

        return goals

    # -------------------------
    # Attention-driven goals
    # -------------------------
    def _from_attention_hotspots(self) -> List[Dict[str, Any]]:
        goals = []

        for signal in getattr(self.attention, "focus_window", []):
            item = signal.item

            if item.get("tags"):
                goals.append({
                    "id": str(uuid.uuid4()),
                    "type": "fanout",
                    "priority": signal.score,
                    "payload": {
                        "modules": ["analyzer", "insight_generator"],
                        "data": item,
                        "source": "attention_hotspot"
                    }
                })

        return goals

    # -------------------------
    # Failure-driven goals
    # -------------------------
    def _from_failure_patterns(self) -> List[Dict[str, Any]]:
        goals = []

        history = getattr(self.orchestrator, "state", {}).event_log if hasattr(self.orchestrator, "state") else []

        failure_count = 0

        for event in history[-50:]:
            if event.event_type.endswith("error") or "fail" in event.event_type:
                failure_count += 1

        if failure_count > 3:
            goals.append({
                "id": str(uuid.uuid4()),
                "type": "pipeline",
                "priority": 5.0,
                "payload": {
                    "steps": [
                        {"module": "diagnostic_analyzer"},
                        {"module": "repair_suggester"}
                    ],
                    "source": "failure_recovery"
                }
            })

        return goals
