# priority_scheduler.py

from typing import List, Dict, Any, Optional
import time
import heapq
import uuid


class ScheduledTask:
    """
    Wraps a TaskNode with execution priority metadata.
    """

    def __init__(
        self,
        task: Dict[str, Any],
        priority: float = 1.0,
        created_at: float = None
    ):
        self.task = task
        self.priority = priority
        self.created_at = created_at or time.time()
        self.task_id = task.get("task_id") or str(uuid.uuid4())

    def __lt__(self, other):
        """
        Heap ordering:
        - higher priority first
        - earlier tasks first if equal priority
        """
        if self.priority == other.priority:
            return self.created_at < other.created_at
        return self.priority > other.priority


class PriorityScheduler:
    """
    Converts GoalPlan → prioritized execution queue.

    Responsibilities:
    - priority scoring
    - dependency awareness (lightweight)
    - queue management
    - task selection for execution
    """

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.queue: List[ScheduledTask] = []

    # -------------------------
    # Ingestion
    # -------------------------
    def ingest_plan(self, plan) -> None:
        """
        Convert GoalPlan into scheduled tasks.
        """
        for task in plan.tasks:
            priority = self._score_task(task.to_dict())

            scheduled = ScheduledTask(
                task=task.to_dict(),
                priority=priority
            )

            heapq.heappush(self.queue, scheduled)

        self.orchestrator._log("plan_scheduled", {
            "task_count": len(plan.tasks)
        })

    # -------------------------
    # Scoring Engine
    # -------------------------
    def _score_task(self, task: Dict[str, Any]) -> float:
        """
        Simple heuristic scoring system.

        You can later replace this with:
        - RL policy
        - LLM scoring
        - reward model
        """

        base = 1.0

        module = task.get("module", "")

        # High-value execution types
        if module in ["insight_generator", "analyzer"]:
            base += 2.0

        if module in ["data_ingestor"]:
            base += 1.5

        # Dependency penalty (defer dependent tasks slightly)
        if task.get("dependencies"):
            base -= 0.3

        # Fanout boost (parallel importance)
        if task.get("metadata", {}).get("fanout_root"):
            base += 1.0

        return base

    # -------------------------
    # Dispatch Interface
    # -------------------------
    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """
        Pop highest-priority ready task.
        """
        if not self.queue:
            return None

        scheduled = heapq.heappop(self.queue)
        return scheduled.task

    # -------------------------
    # Queue Inspection
    # -------------------------
    def peek(self) -> Optional[Dict[str, Any]]:
        if not self.queue:
            return None
        return self.queue[0].task

    def size(self) -> int:
        return len(self.queue)

    # -------------------------
    # Dynamic Reprioritisation
    # -------------------------
    def reprioritize(self, task_id: str, new_priority: float):
        """
        Rebuild queue with updated priority.
        (Simple version; can be optimised later)
        """
        tasks = []

        while self.queue:
            tasks.append(heapq.heappop(self.queue))

        for t in tasks:
            if t.task_id == task_id:
                t.priority = new_priority

        for t in tasks:
            heapq.heappush(self.queue, t)

        self.orchestrator._log("task_reprioritized", {
            "task_id": task_id,
            "new_priority": new_priority
        })
