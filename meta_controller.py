# meta_controller.py

from typing import Dict, Any, List
import time


class MetaController:
    """
    Top-level governance layer for RSIForge.

    Controls system-wide behavior:
    - attention intensity
    - goal emergence rate
    - reflection frequency
    - execution aggressiveness
    - subsystem biasing

    This is NOT execution logic.
    This is system cognition control.
    """

    def __init__(
        self,
        orchestrator,
        autonomous_loop,
        attention_router,
        reflection_engine,
        goal_emergence_engine
    ):
        self.orchestrator = orchestrator
        self.loop = autonomous_loop
        self.attention = attention_router
        self.reflection = reflection_engine
        self.goal_engine = goal_emergence_engine

        self.mode = "balanced"

        self.system_pressure = {
            "error_rate": 0.0,
            "queue_depth": 0,
            "memory_growth": 0.0,
            "attention_entropy": 0.0
        }

    # -------------------------
    # Main Control Tick
    # -------------------------
    def tick(self):
        """
        Runs periodically inside or above AutonomousLoop.
        Adjusts system-wide parameters.
        """

        self._collect_signals()
        self._decide_mode()
        self._apply_controls()

        self.orchestrator._log("meta_tick", {
            "mode": self.mode,
            "pressure": self.system_pressure
        })

    # -------------------------
    # Signal Collection
    # -------------------------
    def _collect_signals(self):
        state = getattr(self.orchestrator, "state", None)

        # approximate system pressure signals
        if state:
            events = getattr(state, "event_log", [])

            errors = sum(1 for e in events[-50:] if "error" in e.event_type)
            total = max(1, len(events[-50:]))

            self.system_pressure["error_rate"] = errors / total

        self.system_pressure["queue_depth"] = getattr(
            getattr(self.loop, "goal_queue", []), "__len__", lambda: 0
        )()

        self.system_pressure["memory_growth"] = len(
            getattr(getattr(self.attention, "memory", {}), "nodes", {})
        )

        # attention entropy proxy
        focus = getattr(self.attention, "focus_window", [])
        self.system_pressure["attention_entropy"] = len(focus)

    # -------------------------
    # Mode Decision Engine
    # -------------------------
    def _decide_mode(self):
        p = self.system_pressure

        if p["error_rate"] > 0.3:
            self.mode = "repair"

        elif p["queue_depth"] > 20:
            self.mode = "execution"

        elif p["attention_entropy"] < 3:
            self.mode = "exploration"

        else:
            self.mode = "balanced"

    # -------------------------
    # System Control Application
    # -------------------------
    def _apply_controls(self):
        """
        Adjust subsystem behavior based on mode.
        """

        if self.mode == "repair":
            self._apply_repair_mode()

        elif self.mode == "execution":
            self._apply_execution_mode()

        elif self.mode == "exploration":
            self._apply_exploration_mode()

        else:
            self._apply_balanced_mode()

    # -------------------------
    # Mode Behaviors
    # -------------------------
    def _apply_repair_mode(self):
        self.loop.tick_interval = 2.0  # slow down
        self.orchestrator._log("mode_switch", {"mode": "repair"})

    def _apply_execution_mode(self):
        self.loop.tick_interval = 0.5  # speed up
        self.orchestrator._log("mode_switch", {"mode": "execution"})

    def _apply_exploration_mode(self):
        self.loop.tick_interval = 1.5
        self.orchestrator._log("mode_switch", {"mode": "exploration"})

        # encourage new goals
        if hasattr(self.goal_engine, "generate_goals"):
            new_goals = self.goal_engine.generate_goals()
            for g in new_goals:
                self.loop.submit_goal(g)

    def _apply_balanced_mode(self):
        self.loop.tick_interval = 1.0
