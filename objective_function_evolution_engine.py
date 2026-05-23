# objective_function_evolution_engine.py

from typing import Dict, Any, List
import uuid
import time


class ObjectiveFunctionProposal:
    """
    A candidate modification to the system's objective function.
    """

    def __init__(self, delta: Dict[str, float], rationale: str, risk: float):
        self.id = str(uuid.uuid4())
        self.delta = delta
        self.rationale = rationale
        self.risk = risk
        self.timestamp = time.time()


class ObjectiveFunctionEvolutionEngine:
    """
    Governs controlled evolution of the system's objective function.

    This is NOT free optimization.
    This is constrained evolution under stability invariants.
    """

    def __init__(self, orchestrator, value_model, truth_engine, meta_cognition):
        self.orchestrator = orchestrator
        self.value_model = value_model
        self.truth_engine = truth_engine
        self.meta = meta_cognition

        self.history: List[ObjectiveFunctionProposal] = []

        # baseline objective weights (must remain anchored)
        self.base_objective = {
            "accuracy": 0.45,
            "speed": 0.25,
            "stability": 0.20,
            "cost": -0.10
        }

    # -------------------------
    # Step 1: Detect misalignment drift
    # -------------------------
    def detect_drift(self) -> Dict[str, Any]:
        """
        Measures whether current objective structure is failing.
        """

        recent = self.truth_engine.history[-20:] if self.truth_engine.history else []

        if not recent:
            return {"drift": 0.0}

        variance = sum(r.get("variance", 0) for r in recent) / len(recent)
        instability = sum(1 for r in recent if r.get("mean_score", 0) < 0)

        drift = variance + instability * 0.1

        return {
            "drift": drift,
            "instability": instability
        }

    # -------------------------
    # Step 2: Propose objective adjustments
    # -------------------------
    def propose_objective_change(self) -> List[ObjectiveFunctionProposal]:
        """
        Suggests bounded changes to objective weights.
        """

        drift_state = self.detect_drift()
        proposals = []

        # If unstable, increase stability weight
        if drift_state["drift"] > 0.5:
            proposals.append(
                ObjectiveFunctionProposal(
                    delta={"stability": +0.05, "speed": -0.02},
                    rationale="Increase stability weighting due to observed drift",
                    risk=0.1
                )
            )

        # If system too slow but stable, rebalance toward speed
        if drift_state["drift"] < 0.2:
            proposals.append(
                ObjectiveFunctionProposal(
                    delta={"speed": +0.03, "accuracy": -0.01},
                    rationale="System is stable; allow efficiency gain",
                    risk=0.2
                )
            )

        self.history.extend(proposals)

        self.orchestrator._log("objective_function_proposals", {
            "count": len(proposals),
            "drift": drift_state["drift"]
        })

        return proposals

    # -------------------------
    # Step 3: Validate safety constraints
    # -------------------------
    def validate(self, proposal: ObjectiveFunctionProposal) -> bool:
        """
        Prevents unstable or destructive objective drift.
        """

        # hard constraint: stability cannot drop too far
        if proposal.delta.get("stability", 0) < -0.05:
            return False

        # risk ceiling
        if proposal.risk > 0.5:
            return False

        return True

    # -------------------------
    # Step 4: Apply bounded evolution
    # -------------------------
    def apply(self, proposal: ObjectiveFunctionProposal) -> Dict[str, float]:
        """
        Applies a safe, bounded update to objective weights.
        """

        if not self.validate(proposal):
            return self.base_objective

        updated = self.base_objective.copy()

        for k, v in proposal.delta.items():
            if k in updated:
                updated[k] += v

        # normalization step (prevents runaway drift)
        total = sum(abs(v) for v in updated.values())

        for k in updated:
            updated[k] = updated[k] / total

        self.value_model.objective_weights = updated

        self.orchestrator._log("objective_function_updated", {
            "new_weights": updated
        })

        return updated
