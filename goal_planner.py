# goal_planner.py

from typing import Dict, Any, List, Optional
import uuid


class TaskNode:
    """
    Atomic unit of work produced by the planner.
    """

    def __init__(
        self,
        module: str,
        payload: Dict[str, Any],
        dependencies: Optional[List[str]] = None,
        task_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.task_id = task_id or str(uuid.uuid4())
        self.module = module
        self.payload = payload
        self.dependencies = dependencies or []
        self.metadata = metadata or {}

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "module": self.module,
            "payload": self.payload,
            "dependencies": self.dependencies,
            "metadata": self.metadata,
        }


class GoalPlan:
    """
    A structured execution graph derived from a single goal.
    """

    def __init__(self, goal: Dict[str, Any]):
        self.goal = goal
        self.tasks: List[TaskNode] = []

    def add_task(self, task: TaskNode):
        self.tasks.append(task)

    def to_dict(self):
        return {
            "goal": self.goal,
            "tasks": [t.to_dict() for t in self.tasks],
        }


class GoalPlanner:
    """
    Translates high-level goals into executable task graphs
    for SwarmRuntime + AutonomousLoop.
    """

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    # -------------------------
    # Entry Point
    # -------------------------
    def plan(self, goal: Dict[str, Any]) -> GoalPlan:
        """
        Main planning interface.
        Converts goal → structured task graph.
        """
        goal_type = goal.get("type")
        payload = goal.get("payload", {})

        plan = GoalPlan(goal)

        # -------------------------
        # ANALYZE / FANOUT GOALS
        # -------------------------
        if goal_type == "analyze":
            plan = self._plan_analyze(goal, payload)

        elif goal_type == "fanout":
            plan = self._plan_fanout(goal, payload)

        elif goal_type == "pipeline":
            plan = self._plan_pipeline(goal, payload)

        elif goal_type == "execute":
            plan = self._plan_execute(goal, payload)

        else:
            plan.add_task(TaskNode(
                module="unknown_handler",
                payload={"goal": goal}
            ))

        # log planning step
        self.orchestrator._log("goal_planned", plan.to_dict())

        return plan

    # -------------------------
    # PLAN TYPES
    # -------------------------
    def _plan_analyze(self, goal: Dict[str, Any], payload: Dict[str, Any]) -> GoalPlan:
        plan = GoalPlan(goal)

        plan.add_task(TaskNode(
            module="data_ingestor",
            payload=payload
        ))

        plan.add_task(TaskNode(
            module="analyzer",
            payload={"input_ref": "data_ingestor"},
            dependencies=[]
        ))

        plan.add_task(TaskNode(
            module="insight_generator",
            payload={"input_ref": "analyzer"},
            dependencies=[]
        ))

        return plan

    def _plan_fanout(self, goal: Dict[str, Any], payload: Dict[str, Any]) -> GoalPlan:
        plan = GoalPlan(goal)

        modules = payload.get("modules", [])
        data = payload.get("data", {})

        root_id = str(uuid.uuid4())

        for m in modules:
            plan.add_task(TaskNode(
                module=m,
                payload=data,
                dependencies=[root_id],
                metadata={"fanout_root": root_id}
            ))

        return plan

    def _plan_pipeline(self, goal: Dict[str, Any], payload: Dict[str, Any]) -> GoalPlan:
        plan = GoalPlan(goal)

        steps = payload.get("steps", [])

        prev_id = None

        for step in steps:
            node = TaskNode(
                module=step.get("module"),
                payload=step.get("payload", {}),
                dependencies=[prev_id] if prev_id else []
            )
            plan.add_task(node)
            prev_id = node.task_id

        return plan

    def _plan_execute(self, goal: Dict[str, Any], payload: Dict[str, Any]) -> GoalPlan:
        plan = GoalPlan(goal)

        plan.add_task(TaskNode(
            module=payload.get("module"),
            payload=payload.get("data", {})
        ))

        return plan
