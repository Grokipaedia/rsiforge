# autonomous_epistemic_boundary_manager.py

from typing import Dict, Any, List
import time
import uuid


class EpistemicBoundary:
    """
    Defines what the system is allowed to know, assume, or optimise.
    """

    def __init__(self, domain: str, status: str, confidence_range: float):
        self.id = str(uuid.uuid4())
        self.domain = domain
        self.status = status  # "known", "uncertain", "unknown", "unmodelled"
        self.confidence_range = confidence_range
        self.created_at = time.time()


class AutonomousEpistemicBoundaryManager:
    """
    Controls the system's epistemic limits.

    Prevents:
    - overconfidence collapse
    - metric overfitting
    - recursive self-delusion loops
    - uncontrolled goal expansion
    """

    def __init__(self, meta_cognition, truth_engine, orchestrator):
        self.meta = meta_cognition
        self.truth_engine = truth_engine
        self.orchestrator = orchestrator

        self.boundaries: List[EpistemicBoundary] = []

        # core invariant zones (cannot be removed)
        self.invariants = {
            "truth_metric_exists": True,
            "evaluation_is_fallible": True,
            "system_is_bounded": True
        }

    # -------------------------
    # Step 1: Observe epistemic drift
    # -------------------------
    def detect_epistemic_drift(self) -> Dict[str, float]:
        """
        Measures whether system is overconfident in uncertain domains.
        """

        logs = self.meta.get_uncertainty_logs()

        if not logs:
            return {"drift": 0.0}

        overconfidence_events = sum(
            1 for l in logs if l.get("confidence") > 0.9 and l.get("error") > 0.5
        )

        drift_score = overconfidence_events / max(len(logs), 1)

        return {
            "epistemic_drift": drift_score,
            "samples": len(logs)
        }

    # -------------------------
    # Step 2: Classify knowledge domains
    # -------------------------
    def classify_domain(self, signal: Dict[str, Any]) -> EpistemicBoundary:
        """
        Assign epistemic status to system knowledge areas.
        """

        confidence = signal.get("confidence", 0.5)
        error = signal.get("error", 0.5)
        domain = signal.get("domain", "unknown")

        if confidence > 0.8 and error < 0.2:
            status = "known"
        elif confidence > 0.5:
            status = "uncertain"
        else:
            status = "unknown"

        return EpistemicBoundary(
            domain=domain,
            status=status,
            confidence_range=confidence - error
        )

    # -------------------------
    # Step 3: Enforce epistemic constraints
    # -------------------------
    def enforce_constraints(self, proposal: Dict[str, Any]) -> bool:
        """
        Blocks unsafe optimization over unknown domains.
        """

        target = proposal.get("target", "")

        forbidden_targets = [
            "truth_definition",
            "objective_function_core",
            "evaluation_axioms"
        ]

        if target in forbidden_targets:
            return False

        return True

    # -------------------------
    # Step 4: Update epistemic map
    # -------------------------
    def update(self, signals: List[Dict[str, Any]]):
        """
        Refreshes system knowledge boundaries.
        """

        for s in signals:
            boundary = self.classify_domain(s)
            self.boundaries.append(boundary)

        self.orchestrator._log("epistemic_boundaries_updated", {
            "count": len(signals)
        })

    # -------------------------
    # Step 5: Validate system proposals
    # -------------------------
    def validate_proposal(self, proposal: Dict[str, Any]) -> bool:
        """
        Final gate preventing epistemic collapse.
        """

        if not self.enforce_constraints(proposal):
            return False

        drift = self.detect_epistemic_drift()

        if drift["epistemic_drift"] > 0.6:
            # system is too unstable to modify core assumptions
            if proposal.get("risk", 0) > 0.2:
                return False

        return True
