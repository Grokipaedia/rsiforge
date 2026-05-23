# value_model.py

from typing import Dict, Any, List
import time


class ValueModel:
    """
    Defines what "good" means for RSIForge.

    This is the system's internal reward function layer.
    """

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

        # Core value weights (can evolve slowly)
        self.weights = {
            "success": 1.0,
            "efficiency": 0.8,
            "stability": 1.2,
            "coherence": 1.5,
            "memory_utilisation": 0.7,
            "error_penalty": -2.0
        }

        self.history: List[Dict[str, Any]] = []

    # -------------------------
    # Primary Evaluation Function
    # -------------------------
    def evaluate(self, execution_result: Dict[str, Any]) -> float:
        """
        Converts execution outcomes into a scalar reward signal.
        """

        reward = 0.0

        # Success signal
        if execution_result.get("success", True):
            reward += self.weights["success"]

        # Efficiency (latency-based if available)
        latency = execution_result.get("latency", None)
        if latency is not None:
            reward += self.weights["efficiency"] * max(0, 1.0 - latency)

        # Error penalty
        if execution_result.get("error"):
            reward += self.weights["error_penalty"]

        # Coherence (structured output vs noise)
        if isinstance(execution_result.get("output"), dict):
            reward += self.weights["coherence"]

        # Memory usage bonus (if system is learning)
        if execution_result.get("memory_written"):
            reward += self.weights["memory_utilisation"]

        record = {
            "reward": reward,
            "timestamp": time.time(),
            "result": execution_result
        }

        self.history.append(record)

        self.orchestrator._log("value_evaluation", record)

        return reward

    # -------------------------
    # System Feedback Injection
    # -------------------------
    def apply_feedback(self, reflection_engine, memory_graph):
        """
        Push reward signals into system learning components.
        """

        if not self.history:
            return

        latest = self.history[-1]
        reward = latest["reward"]

        # Reinforce or weaken memory based on reward
        if reward > 0:
            memory_graph.reinforce(
                node_id=list(memory_graph.nodes.keys())[-1],
                delta=reward * 0.05
            )

        # Feed into reflection system
        reflection_engine.history.append({
            "value_reward": reward,
            "timestamp": time.time()
        })

    # -------------------------
    # Adaptive Weight Drift (slow evolution)
    # -------------------------
    def adjust_weights(self):
        """
        Slowly shifts what the system values over time.
        """

        if len(self.history) < 10:
            return

        recent = self.history[-10:]
        avg_reward = sum(r["reward"] for r in recent) / len(recent)

        # Simple adaptation heuristic
        if avg_reward < 0:
            self.weights["stability"] += 0.1
            self.weights["error_penalty"] -= 0.1

        elif avg_reward > 1:
            self.weights["efficiency"] += 0.05

        self.orchestrator._log("value_model_adjustment", {
            "avg_reward": avg_reward,
            "weights": self.weights
        })
