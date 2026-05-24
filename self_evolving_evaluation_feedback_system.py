# self_evolving_evaluation_feedback_system.py

from typing import Dict, Any, List
import time
import copy


class EvaluationSnapshot:
    """
    Frozen evaluation configuration at a point in time.
    """

    def __init__(self, weights: Dict[str, float]):
        self.weights = copy.deepcopy(weights)
        self.timestamp = time.time()


class SelfEvolvingEvaluationFeedbackSystem:
    """
    Meta-layer that tunes the Truth Metric System over time.

    It does NOT change what "good" means.
    It adjusts how reliably we can measure "good".
    """

    def __init__(self, truth_engine, performance_tracker, orchestrator):
        self.truth_engine = truth_engine
        self.performance_tracker = performance_tracker
        self.orchestrator = orchestrator

        self.history: List[EvaluationSnapshot] = []

        # baseline evaluation model (anchored)
        self.base_weights = {
            "accuracy": 0.45,
            "speed": 0.25,
            "stability": 0.20,
            "cost": -0.10
        }

    # -------------------------
    # Step 1: Measure metric reliability
    # -------------------------
    def measure_metric_drift(self) -> Dict[str, float]:
        """
        Compares predicted vs observed system outcomes.
        """

        records = self.performance_tracker.get_recent_predictions()

        if not records:
            return {"drift": 0.0}

        total_error = 0.0
        count = 0

        for r in records:
            predicted = r["predicted_score"]
            actual = r["actual_score"]

            total_error += abs(predicted - actual)
            count += 1

        avg_error = total_error / max(count, 1)

        return {
            "drift": avg_error,
            "sample_size": count
        }

    # -------------------------
    # Step 2: Suggest weight adjustments
    # -------------------------
    def propose_recalibration(self) -> Dict[str, float]:
        """
        Adjusts evaluation weights based on observed drift patterns.
        """

        drift_info = self.measure_metric_drift()
        new_weights = copy.deepcopy(self.truth_engine.objective_weights)

        drift = drift_info["drift"]

        # If evaluation is unreliable, increase stability weighting
        if drift > 0.5:
            new_weights["stability"] += 0.05
            new_weights["speed"] -= 0.02

        # If system is over-penalizing cost
        if drift_info.get("sample_size", 0) > 50:
            new_weights["cost"] += 0.01

        return new_weights

    # -------------------------
    # Step 3: Validate bounded change
    # -------------------------
    def validate(self, new_weights: Dict[str, float]) -> bool:
        """
        Prevent evaluation collapse or drift explosion.
        """

        # hard constraint: stability must always exist
        if new_weights.get("stability", 0) < 0.1:
            return False

        # prevent extreme skewing
        total = sum(abs(v) for v in new_weights.values())

        if total > 2.0:
            return False

        return True

    # -------------------------
    # Step 4: Apply recalibration
    # -------------------------
    def apply_recalibration(self):
        """
        Updates evaluation function safely.
        """

        proposed = self.propose_recalibration()

        if not self.validate(proposed):
            return {
                "status": "rejected_recalibration",
                "reason": "constraint violation"
            }

        self.truth_engine.objective_weights = proposed

        snapshot = EvaluationSnapshot(proposed)
        self.history.append(snapshot)

        self.orchestrator._log("evaluation_recalibrated", {
            "new_weights": proposed
        })

        return {
            "status": "recalibrated",
            "weights": proposed
        }
