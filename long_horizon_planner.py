# long_horizon_planner.py

from typing import Dict, Any, List, Optional
import time
import uuid


class HorizonGoal:
    """
    A goal that persists across multiple autonomous cycles.
    """

    def __init__(
        self,
        objective: str,
        priority: float = 1.0,
        steps: Optional[List[Dict[str, Any]]] = None,
        horizon: int = 10
    ):
        self.id = str(uuid.uuid4())
        self.objective = objective
        self.priority = priority
        self.steps = steps or []
        self.horizon = horizon  # number of loop cycles expected
        self.created_at = time.time()
        self.progress = 0.0


class LongHorizonPlanner:
    """
    Maintains persistent goals across multiple execution cycles.

    Adds:
    - cross-cycle planning
    - delayed execution reasoning
    - progress tracking
    - goal persistence pressure
    """

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.active_goals: Dict[str, HorizonGoal] = {}

    # -------------------------
    # Create Long-Horizon Goal
    # -------------------------
    def create_goal(
        self,
        objective: str,
        priority: float = 1.0,
        horizon: int = 10
    ) -> HorizonGoal:

        goal = HorizonGoal(
            objective=objective,
            priority=priority,
            horizon=horizon
        )

        self.active_goals[goal.id] = goal

        self.orchestrator._log("long_horizon_goal_created", {
            "goal_id": goal.id,
            "objective": objective,
            "horizon": horizon
        })

        return goal

    # -------------------------
    # Step Expansion
    # -------------------------
    def expand_goal(self, goal_id: str, planner_fn):
        """
        Expands a high-level goal into structured steps.
        """

        goal = self.active_goals.get(goal_id)
        if not goal:
            return None

        goal.steps = planner_fn(goal.objective)

        self.orchestrator._log("long_horizon_goal_expanded", {
            "goal_id": goal_id,
            "step_count": len(goal.steps)
        })

        return goal.steps

    # -------------------------
    # Cycle Update
    # -------------------------
    def tick(self, execution_feedback: List[Dict[str, Any]]):
        """
        Updates long-term goals based on execution results.
        """

        for goal in self.active_goals.values():

            # reduce horizon pressure each cycle
            goal.horizon -= 1

            # update progress heuristically
            completed_steps = sum(
                1 for s in goal.steps if s.get("completed")
            )

            if goal.steps:
                goal.progress = completed_steps / len(goal.steps)

            # decay priority if stagnant
            if goal.horizon <= 0 and goal.progress < 1.0:
                goal.priority *= 0.8

            self.orchestrator._log("long_horizon_tick", {
                "goal_id": goal.id,
                "progress": goal.progress,
                "remaining_horizon": goal.horizon
            })

    # -------------------------
    # Active Goal Selection
    # -------------------------
    def get_active_goals(self) -> List[Dict[str, Any]]:
        """
        Returns prioritized long-term goals for injection into system.
        """

        sorted_goals = sorted(
            self.active_goals.values(),
            key=lambda g: (g.priority, g.progress),
            reverse=True
        )

        return [
            {
                "id": g.id,
                "objective": g.objective,
                "priority": g.priority,
                "progress": g.progress,
                "horizon": g.horizon
            }
            for g in sorted_goals
        ]

    # -------------------------
    # Goal Completion Cleanup
    # -------------------------
    def prune_completed(self):
        """
        Removes finished or irrelevant long-term goals.
        """

        to_remove = []

        for gid, goal in self.active_goals.items():
            if goal.progress >= 1.0:
                to_remove.append(gid)

        for gid in to_remove:
            del self.active_goals[gid]

            self.orchestrator._log("long_horizon_goal_completed", {
                "goal_id": gid
            })
