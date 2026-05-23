# reflection_engine.py

from typing import Dict, Any, List
import time


class ReflectionEngine:
    """
    Evaluates execution outcomes and updates system cognition signals.

    This is the first true "learning loop" layer in RSIForge.
    """

    def __init__(self, orchestrator, memory_graph, attention_router):
        self.orchestrator = orchestrator
        self.memory = memory_graph
        self.attention = attention_router

        self.history: List[Dict[str, Any]] = []

    # -------------------------
    # Core Reflection Cycle
    # -------------------------
    def reflect(self, execution_batch: Dict[str, Any]):
        """
        execution_batch format:
        {
            "tasks": [...],
            "results": [...],
            "graph_snapshot": {...}
        }
        """

        tasks = execution_batch.get("tasks", [])
        results = execution_batch.get("results", [])

        for task, result in zip(tasks, results):
            score = self._score_result(task, result)

            self._update_memory(task, result, score)
            self._update_attention_bias(task, score)

            self.history.append({
                "task": task,
                "score": score,
                "timestamp": time.time()
            })

        self.orchestrator._log("reflection_cycle_complete", {
            "task_count": len(tasks)
        })

    # -------------------------
    # Outcome Scoring
    # -------------------------
    def _score_result(self, task: Dict[str, Any], result: Any) -> float:
        """
        Simple heuristic evaluation function.

        Later upgrade point:
        - LLM evaluator
        - reward model
        - user feedback signal
        """

        if result is None:
            return -1.0

        score = 1.0

        # success signal
        if isinstance(result, dict) and result.get("error"):
            score -= 1.5

        # completeness heuristic
        if isinstance(result, dict) and len(result) > 0:
            score += 0.5

        # dependency quality signal
        if task.get("dependencies"):
            score += 0.2

        return score

    # -------------------------
    # Memory Reinforcement
    # -------------------------
    def _update_memory(self, task: Dict[str, Any], result: Any, score: float):
        """
        Strengthen or weaken memory nodes based on outcome.
        """

        tags = task.get("metadata", {}).get("tags", [])

        node_id = self.memory.write(
            content={
                "task": task,
                "result": result,
                "score": score
            },
            tags=tags + ["reflection"]
        )

        if score > 0:
            self.memory.reinforce(node_id, delta=score * 0.1)

    # -------------------------
    # Attention Adjustment
    # -------------------------
    def _update_attention_bias(self, task: Dict[str, Any], score: float):
        """
        Adjusts future focus pressure indirectly.
        """

        tags = task.get("metadata", {}).get("tags", [])

        if score < 0:
            # negative bias: reduce attention weight on failing patterns
            for t in tags:
                self.attention.orchestrator._log(
                    "attention_penalty_signal",
                    {"tag": t, "score": score}
                )
