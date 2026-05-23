# memory_context_adapter.py

from typing import Dict, Any, List


class MemoryContextAdapter:
    """
    Bridges MemoryGraph → GoalPlanner + SwarmRuntime.

    Purpose:
    - inject relevant memory into planning
    - expand goals using past context
    - bias execution based on history
    """

    def __init__(self, memory_graph, orchestrator):
        self.memory = memory_graph
        self.orchestrator = orchestrator

    # -------------------------
    # Context Enrichment
    # -------------------------
    def enrich_goal(self, goal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Expands a goal using memory associations.
        """

        tags = goal.get("tags", [])
        enriched_context = []

        for tag in tags:
            results = self.memory.query_by_tag(tag)
            enriched_context.extend(results[:3])  # top-k

        goal["memory_context"] = enriched_context

        self.orchestrator._log("goal_enriched_with_memory", {
            "tags": tags,
            "hits": len(enriched_context)
        })

        return goal

    # -------------------------
    # Context Injection into Tasks
    # -------------------------
    def inject_task_context(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attaches relevant memory to execution payload.
        """

        tags = task.get("metadata", {}).get("tags", [])
        context = []

        for tag in tags:
            context.extend(self.memory.query_by_tag(tag))

        task.setdefault("payload", {})
        task["payload"]["memory_context"] = context

        return task

    # -------------------------
    # Feedback Loop (VERY IMPORTANT)
    # -------------------------
    def store_execution_result(self, task: Dict[str, Any], result: Any):
        """
        Writes execution outcomes back into memory graph.
        """

        content = {
            "task": task,
            "result": result
        }

        node_id = self.memory.write(
            content=content,
            tags=["execution_result"] + task.get("metadata", {}).get("tags", [])
        )

        return node_id
