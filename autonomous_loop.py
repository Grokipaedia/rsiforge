# autonomous_loop.py

from typing import Dict, Any, List, Callable, Optional
import time
import threading


class AutonomousLoop:
    """
    The execution heartbeat of RSIForge.

    Responsibilities:
    - Continuously processes goals or events
    - Dispatches work to swarm runtime
    - Updates memory via orchestrator
    - Maintains loop state + stop conditions
    """

    def __init__(
        self,
        orchestrator,
        swarm_runtime,
        tick_interval: float = 1.0
    ):
        self.orchestrator = orchestrator
        self.swarm = swarm_runtime
        self.tick_interval = tick_interval

        self.running = False
        self.thread = None

        self.goal_queue: List[Dict[str, Any]] = []
        self.event_hooks: List[Callable] = []

    # -------------------------
    # Lifecycle
    # -------------------------
    def start(self):
        """Start autonomous execution loop."""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop execution loop."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)

    # -------------------------
    # Goal Injection
    # -------------------------
    def submit_goal(self, goal: Dict[str, Any]):
        """
        Push a new goal into the system.

        Example:
        {
            "type": "analyze",
            "payload": {...},
            "priority": 1
        }
        """
        self.goal_queue.append(goal)

    # -------------------------
    # Event Hooks
    # -------------------------
    def register_hook(self, fn: Callable):
        """
        Register function that receives loop ticks.
        """
        self.event_hooks.append(fn)

    # -------------------------
    # Core Loop
    # -------------------------
    def _run_loop(self):
        while self.running:
            start = time.time()

            # 1. Handle events/hooks
            self._run_hooks()

            # 2. Process next goal
            if self.goal_queue:
                goal = self.goal_queue.pop(0)
                self._process_goal(goal)

            # 3. Tick pacing
            elapsed = time.time() - start
            sleep_time = max(0, self.tick_interval - elapsed)
            time.sleep(sleep_time)

    # -------------------------
    # Hook Execution
    # -------------------------
    def _run_hooks(self):
        for hook in self.event_hooks:
            try:
                hook(self.orchestrator.state)
            except Exception:
                # isolate hook failure
                continue

    # -------------------------
    # Goal Processing
    # -------------------------
    def _process_goal(self, goal: Dict[str, Any]):
        """
        Converts a goal into swarm tasks.
        """

        goal_type = goal.get("type")
        payload = goal.get("payload", {})

        # Simple routing logic (expandable into planner later)
        if goal_type == "fanout":
            modules = payload.get("modules", [])
            data = payload.get("data", {})

            tasks = [
                self.swarm.broadcast(modules, data)
            ]

            # flatten broadcast result (single batch)
            results = tasks[0]

            self.orchestrator._log("goal_complete", {
                "goal": goal,
                "results": [r.module_name for r in results]
            })

        elif goal_type == "execute":
            module = payload.get("module")
            data = payload.get("data", {})

            result = self.orchestrator.run(module, data)

            self.orchestrator._log("goal_execute", {
                "goal": goal,
                "result": result
            })

        elif goal_type == "reduce":
            module_list = payload.get("modules", [])
            data = payload.get("data", {})
            reducer = payload.get("reducer")

            results = self.swarm.broadcast(module_list, data)
            final = self.swarm.reduce(results, reducer)

            self.orchestrator._log("goal_reduce", {
                "goal": goal,
                "output": final
            })

        else:
            self.orchestrator._log("goal_unknown", {"goal": goal})
