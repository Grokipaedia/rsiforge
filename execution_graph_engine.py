# execution_graph_engine.py

from typing import Dict, Any, List, Set, Optional
import time
import uuid
from collections import defaultdict, deque


class GraphNode:
    """
    Node in the execution DAG.
    """

    def __init__(
        self,
        task: Dict[str, Any],
        node_id: Optional[str] = None
    ):
        self.node_id = node_id or task.get("task_id") or str(uuid.uuid4())
        self.task = task
        self.dependencies: Set[str] = set(task.get("dependencies", []))
        self.dependents: Set[str] = set()
        self.completed = False
        self.result = None
        self.created_at = time.time()


class ExecutionGraph:
    """
    DAG representation of a GoalPlan.

    Handles:
    - dependency tracking
    - execution readiness
    - result propagation
    - graph state updates
    """

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.nodes: Dict[str, GraphNode] = {}

    # -------------------------
    # Build Graph
    # -------------------------
    def build(self, tasks: List[Dict[str, Any]]):
        """
        Convert flat task list into DAG structure.
        """
        for t in tasks:
            node = GraphNode(t)
            self.nodes[node.node_id] = node

        # build reverse edges
        for node in self.nodes.values():
            for dep_id in node.dependencies:
                if dep_id in self.nodes:
                    self.nodes[dep_id].dependents.add(node.node_id)

        self.orchestrator._log("graph_built", {
            "node_count": len(self.nodes)
        })

    # -------------------------
    # Execution Readiness
    # -------------------------
    def get_ready_nodes(self) -> List[GraphNode]:
        """
        Return nodes whose dependencies are satisfied.
        """
        ready = []

        for node in self.nodes.values():
            if node.completed:
                continue

            if all(
                self._is_completed(dep)
                for dep in node.dependencies
            ):
                ready.append(node)

        return ready

    def _is_completed(self, node_id: str) -> bool:
        node = self.nodes.get(node_id)
        return node.completed if node else True

    # -------------------------
    # Execution Update
    # -------------------------
    def mark_complete(self, node_id: str, result: Any):
        node = self.nodes.get(node_id)
        if not node:
            return

        node.completed = True
        node.result = result

        self.orchestrator._log("node_completed", {
            "node_id": node_id
        })

    # -------------------------
    # Graph State Checks
    # -------------------------
    def is_complete(self) -> bool:
        return all(n.completed for n in self.nodes.values())

    def pending_count(self) -> int:
        return sum(1 for n in self.nodes.values() if not n.completed)

    # -------------------------
    # Critical Path Extraction (lightweight)
    # -------------------------
    def get_critical_nodes(self) -> List[GraphNode]:
        """
        Heuristic: nodes with most dependents = higher criticality.
        """
        return sorted(
            self.nodes.values(),
            key=lambda n: len(n.dependents),
            reverse=True
        )

    # -------------------------
    # Execution Snapshot
    # -------------------------
    def snapshot(self) -> Dict[str, Any]:
        return {
            "nodes": {
                nid: {
                    "task": n.task,
                    "completed": n.completed,
                    "dependencies": list(n.dependencies),
                    "dependents": list(n.dependents),
                }
                for nid, n in self.nodes.items()
            }
        }
