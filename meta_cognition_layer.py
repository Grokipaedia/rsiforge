# meta_cognition_layer.py

from typing import Dict, Any, List
import time


class MetaCognitionLayer:
    """
    Observes and evaluates the system's own cognitive processes.

    This is cognition about cognition:
    - not tasks
    - not memory
    - not execution
    but *thinking itself*
    """

    def __init__(
        self,
        orchestrator,
        attention_router,
        reflection_engine,
        meta_controller,
        value_model,
        compression_layer,
        long_horizon_planner
    ):
        self.orchestrator = orchestrator

        self.attention = attention_router
        self.reflection = reflection_engine
        self.meta = meta_controller
        self.value = value_model
        self.compression = compression_layer
        self.horizon = long_horizon_planner

        self.history: List[Dict[str, Any]] = []

    # -------------------------
    # Cognitive State Analysis
    # -------------------------
    def analyse(self) -> Dict[str, Any]:
        """
        Builds a snapshot of the system's cognitive behavior.
        """

        attention_load = len(getattr(self.attention, "focus_window", []))

        recent_reflections = getattr(self.reflection, "history", [])[-20:]
        avg_reward = (
            sum(r.get("value_reward", 0) for r in recent_reflections)
            / max(1, len(recent_reflections))
        )

        compression_pressure = len(getattr(self.compression, "compressed_nodes", {}))

        long_term_pressure = len(self.horizon.active_goals)

        state = {
            "attention_load": attention_load,
            "avg_reward": avg_reward,
            "compression_pressure": compression_pressure,
            "long_term_pressure": long_term_pressure,
            "mode": self.meta.mode
        }

        return state

    # -------------------------
    # Cognitive Mode Detection
    # -------------------------
    def detect_mode(self, state: Dict[str, Any]) -> str:
        """
        Classifies system cognition mode.
        """

        if state["avg_reward"] < -0.5:
            return "collapse_risk"

        if state["attention_load"] > 12:
            return "overfocused"

        if state["compression_pressure"] > 50:
            return "overcompressed"

        if state["long_term_pressure"] > 20:
            return "strategic_overload"

        if state["avg_reward"] > 1.0:
            return "high_performance"

        return "balanced"

    # -------------------------
    # Cognitive Correction Suggestions
    # -------------------------
    def suggest_adjustments(self, mode: str) -> Dict[str, Any]:
        """
        Produces system-wide cognitive tuning recommendations.
        """

        if mode == "collapse_risk":
            return {
                "meta_mode": "repair",
                "reduce_exploration": True,
                "increase_reflection": True
            }

        if mode == "overfocused":
            return {
                "attention_diversity_boost": True,
                "inject_new_goals": True
            }

        if mode == "overcompressed":
            return {
                "decompression_needed": True,
                "memory_expansion_allowed": True
            }

        if mode == "strategic_overload":
            return {
                "reduce_long_horizon_goals": True,
                "prioritise_execution": True
            }

        if mode == "high_performance":
            return {
                "reinforce_current_policy": True
            }

        return {
            "maintain_current_state": True
        }

    # -------------------------
    # Apply Meta-Cognitive Feedback
    # -------------------------
    def apply(self):
        """
        Main loop: observe → classify → adjust cognition.
        """

        state = self.analyse()
        mode = self.detect_mode(state)
        suggestion = self.suggest_adjustments(mode)

        # feed into meta controller
        self.meta.mode = suggestion.get("meta_mode", self.meta.mode)

        # adjust system behaviour signals
        if suggestion.get("reduce_exploration"):
            self.horizon.active_goals = self.horizon.active_goals[:10]

        if suggestion.get("decompression_needed"):
            self.compression.run()

        if suggestion.get("inject_new_goals"):
            self.orchestrator._log("meta_goal_injection_suggested", {})

        self.history.append({
            "state": state,
            "mode": mode,
            "suggestion": suggestion,
            "timestamp": time.time()
        })

        self.orchestrator._log("meta_cognition_tick", {
            "mode": mode,
            "state": state
        })

        return suggestion
