# attention_router.py

from typing import Dict, Any, List, Optional
import time
import math


class AttentionSignal:
    """
    Represents a scored memory or task candidate.
    """

    def __init__(self, item: Dict[str, Any], score: float, source: str):
        self.item = item
        self.score = score
        self.source = source
        self.timestamp = time.time()


class AttentionRouter:
    """
    Selective focus engine for RSIForge.

    Responsibilities:
    - rank memory relevance
    - prioritize execution candidates
    - bias planning inputs
    - simulate "working attention window"
    """

    def __init__(self, memory_graph, orchestrator):
        self.memory = memory_graph
        self.orchestrator = orchestrator

        self.focus_window: List[AttentionSignal] = []
        self.max_focus = 10

    # -------------------------
    # Core Attention Scoring
    # -------------------------
    def score_memory(self, memory_item: Dict[str, Any], query_tags: List[str]) -> float:
        """
        Heuristic attention scoring function.
        """

        base = memory_item.get("weight", 1.0)

        tags = set(memory_item.get("tags", []))
        overlap = len(tags.intersection(set(query_tags)))

        recency_boost = 0.0

        # simulate recency if available
        if "timestamp" in memory_item:
            age = time.time() - memory_item["timestamp"]
            recency_boost = max(0.0, 1.0 - (age / 100000))

        score = base + (overlap * 2.0) + recency_boost

        return score

    # -------------------------
    # Memory Attention Selection
    # -------------------------
    def focus_memory(self, query_tags: List[str]) -> List[Dict[str, Any]]:
        """
        Returns top-K most relevant memory nodes.
        """

        candidates = []

        for node_id, node in self.memory.nodes.items():
            item = {
                "id": node_id,
                "content": node.content,
                "tags": list(node.tags),
                "weight": node.weight,
                "timestamp": node.created_at
            }

            score = self.score_memory(item, query_tags)

            candidates.append(
                AttentionSignal(item, score, source="memory")
            )

        # sort by attention score
        candidates.sort(key=lambda x: x.score, reverse=True)

        self.focus_window = candidates[:self.max_focus]

        self.orchestrator._log("attention_memory_focus", {
            "top": [
                {"id": c.item["id"], "score": c.score}
                for c in self.focus_window
            ]
        })

        return [c.item for c in self.focus_window]

    # -------------------------
    # Task Attention Ranking
    # -------------------------
    def focus_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Prioritise execution candidates dynamically.
        """

        ranked = []

        for t in tasks:
            base = 1.0

            # priority hint
            base += t.get("priority", 1.0)

            # dependency pressure (more deps = later focus)
            deps = len(t.get("dependencies", []))
            base -= deps * 0.2

            # memory context boost
            mem_ctx = t.get("payload", {}).get("memory_context", [])
            base += len(mem_ctx) * 0.3

            ranked.append((base, t))

        ranked.sort(key=lambda x: x[0], reverse=True)

        focused = [t for _, t in ranked[:self.max_focus]]

        self.orchestrator._log("attention_task_focus", {
            "focused_count": len(focused)
        })

        return focused

    # -------------------------
    # Dynamic Focus Window Update
    # -------------------------
    def update_focus(self, context_tags: List[str]) -> None:
        """
        Refreshes attention window continuously.
        """

        self.focus_memory(context_tags)

    # -------------------------
    # Attention Compression (optional abstraction layer)
    # -------------------------
    def compress_focus(self) -> Dict[str, Any]:
        """
        Reduces focus window into a single summary signal.
        """

        if not self.focus_window:
            return {}

        combined = {
            "top_signals": len(self.focus_window),
            "dominant_tags": self._extract_dominant_tags(),
            "avg_score": sum(c.score for c in self.focus_window) / len(self.focus_window)
        }

        return combined

    def _extract_dominant_tags(self) -> List[str]:
        tag_counts = {}

        for c in self.focus_window:
            for t in c.item.get("tags", []):
                tag_counts[t] = tag_counts.get(t, 0) + 1

        return sorted(tag_counts, key=tag_counts.get, reverse=True)[:5]
