# distributed_swarm_kernel.py

from typing import Dict, Any, List, Optional
import time
import uuid


class SwarmNode:
    """
    Represents a single cognitive kernel instance.
    """

    def __init__(self, kernel_id: Optional[str] = None):
        self.kernel_id = kernel_id or str(uuid.uuid4())
        self.load = 0.0
        self.last_heartbeat = time.time()
        self.local_state = {}
        self.active = True


class DistributedSwarmKernel:
    """
    Coordinates multiple KernelUnification instances.

    This is NOT execution logic.
    It is:
    - task distribution
    - coordination strategy
    - shared cognition alignment
    - system-level load balancing
    """

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

        self.nodes: Dict[str, SwarmNode] = {}
        self.shared_memory: Dict[str, Any] = {}
        self.global_task_queue: List[Dict[str, Any]] = []

        self.leader_id: Optional[str] = None

    # -------------------------
    # Node Management
    # -------------------------
    def register_node(self, kernel_id: str):
        node = SwarmNode(kernel_id)
        self.nodes[kernel_id] = node

        if not self.leader_id:
            self.leader_id = kernel_id

        self.orchestrator._log("swarm_node_registered", {
            "kernel_id": kernel_id
        })

    def remove_node(self, kernel_id: str):
        if kernel_id in self.nodes:
            del self.nodes[kernel_id]

        if self.leader_id == kernel_id:
            self._elect_new_leader()

    # -------------------------
    # Leader Election (lightweight heuristic)
    # -------------------------
    def _elect_new_leader(self):
        if not self.nodes:
            self.leader_id = None
            return

        # lowest load becomes leader
        self.leader_id = min(
            self.nodes.values(),
            key=lambda n: n.load
        ).kernel_id

        self.orchestrator._log("swarm_leader_elected", {
            "leader": self.leader_id
        })

    # -------------------------
    # Task Distribution
    # -------------------------
    def submit_global_task(self, task: Dict[str, Any]):
        self.global_task_queue.append(task)

    def dispatch(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Distributes tasks across swarm nodes.
        """

        distribution: Dict[str, List[Dict[str, Any]]] = {
            node_id: []
            for node_id in self.nodes
        }

        if not self.nodes:
            return distribution

        for task in self.global_task_queue:
            target = self._select_node(task)
            distribution[target].append(task)

            # update load
            self.nodes[target].load += 0.1

        self.global_task_queue.clear()

        self.orchestrator._log("swarm_dispatch", {
            "distribution": {k: len(v) for k, v in distribution.items()}
        })

        return distribution

    # -------------------------
    # Node Selection Strategy
    # -------------------------
    def _select_node(self, task: Dict[str, Any]) -> str:
        """
        Chooses best kernel for task execution.
        """

        # simplest strategy: lowest load wins
        return min(
            self.nodes.values(),
            key=lambda n: n.load
        ).kernel_id

    # -------------------------
    # Shared Memory Sync
    # -------------------------
    def sync_memory(self, kernel_id: str, data: Dict[str, Any]):
        """
        Merge local kernel memory into global swarm memory.
        """

        self.shared_memory.setdefault(kernel_id, {}).update(data)

        self.orchestrator._log("swarm_memory_sync", {
            "kernel_id": kernel_id,
            "keys": list(data.keys())
        })

    # -------------------------
    # Global Context Broadcast
    # -------------------------
    def broadcast_context(self) -> Dict[str, Any]:
        """
        Sends shared memory state to all kernels.
        """

        context = {
            "global_memory": self.shared_memory,
            "leader": self.leader_id,
            "node_count": len(self.nodes)
        }

        return context

    # -------------------------
    # Health Monitoring
    # -------------------------
    def heartbeat(self, kernel_id: str):
        if kernel_id in self.nodes:
            node = self.nodes[kernel_id]
            node.last_heartbeat = time.time()

    def prune_dead_nodes(self, timeout: float = 30.0):
        """
        Removes inactive kernels.
        """

        now = time.time()
        to_remove = []

        for k, node in self.nodes.items():
            if now - node.last_heartbeat > timeout:
                to_remove.append(k)

        for k in to_remove:
            del self.nodes[k]

            self.orchestrator._log("swarm_node_removed", {
                "kernel_id": k
            })
