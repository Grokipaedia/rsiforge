# persistent_swarm_memory.py

from typing import Dict, Any, List, Optional
import time
import json
import os


class PersistentSwarmMemory:
    """
    Durable memory layer for DistributedSwarmKernel.

    Provides:
    - cross-kernel persistence
    - disk-backed shared cognition
    - replayable system history
    - long-term swarm continuity
    """

    def __init__(self, orchestrator, storage_path: str = "swarm_memory.json"):
        self.orchestrator = orchestrator
        self.storage_path = storage_path

        # in-memory cache
        self.memory: Dict[str, Any] = self._load()

    # -------------------------
    # Load / Save Layer
    # -------------------------
    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.storage_path):
            return {
                "nodes": {},
                "events": [],
                "meta": {
                    "created": time.time()
                }
            }

        with open(self.storage_path, "r") as f:
            return json.load(f)

    def _save(self):
        with open(self.storage_path, "w") as f:
            json.dump(self.memory, f, indent=2)

    # -------------------------
    # Swarm Node Persistence
    # -------------------------
    def write_node(self, kernel_id: str, data: Dict[str, Any]):
        """
        Stores kernel-local memory into global persistent store.
        """

        self.memory["nodes"].setdefault(kernel_id, {})

        for k, v in data.items():
            self.memory["nodes"][kernel_id][k] = v

        self._append_event({
            "type": "node_write",
            "kernel_id": kernel_id,
            "timestamp": time.time(),
            "keys": list(data.keys())
        })

        self._save()

        self.orchestrator._log("persistent_memory_write", {
            "kernel_id": kernel_id
        })

    # -------------------------
    # Read Global State
    # -------------------------
    def read_node(self, kernel_id: str) -> Dict[str, Any]:
        return self.memory["nodes"].get(kernel_id, {})

    def read_global(self) -> Dict[str, Any]:
        return self.memory

    # -------------------------
    # Event Logging
    # -------------------------
    def _append_event(self, event: Dict[str, Any]):
        self.memory["events"].append(event)

        # prevent unbounded growth
        if len(self.memory["events"]) > 10000:
            self.memory["events"] = self.memory["events"][-5000:]

    # -------------------------
    # Cross-Kernel Aggregation
    # -------------------------
    def aggregate(self, key: str) -> Dict[str, Any]:
        """
        Combines values of a key across all kernels.
        """

        result = {}

        for kernel_id, data in self.memory["nodes"].items():
            if key in data:
                result[kernel_id] = data[key]

        return result

    # -------------------------
    # Replay Capability
    # -------------------------
    def replay_events(self, last_n: int = 100) -> List[Dict[str, Any]]:
        """
        Reconstruct recent swarm activity history.
        """

        return self.memory["events"][-last_n:]

    # -------------------------
    # Memory Reinforcement
    # -------------------------
    def reinforce(self, kernel_id: str, key: str, delta: float):
        """
        Adjusts importance signal for persistent memory fields.
        """

        node = self.memory["nodes"].setdefault(kernel_id, {})

        node.setdefault(key, 0.0)
        node[key] += delta

        self._append_event({
            "type": "reinforcement",
            "kernel_id": kernel_id,
            "key": key,
            "delta": delta,
            "timestamp": time.time()
        })

        self._save()
