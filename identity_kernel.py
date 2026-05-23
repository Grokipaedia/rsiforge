# identity_kernel.py

from typing import Dict, Any, List, Set
import time
import copy


class IdentityKernel:
    """
    Persistent identity + constraint system for RSIForge.

    This is NOT execution logic.

    It defines:
    - system "self-concept"
    - invariants that must remain stable
    - drift detection across time
    - behavioral consistency enforcement
    """

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

        # Core identity definition
        self.identity = {
            "name": "RSIForge",
            "type": "autonomous_cognitive_system",
            "principles": [
                "coherence_over_speed",
                "structure_over_ad_hoc_behavior",
                "memory_preservation",
                "attention_efficiency",
                "controlled_autonomy"
            ],
            "allowed_modes": ["balanced", "execution", "exploration", "repair"],
        }

        # Invariants = things system must never violate
        self.invariants: Set[str] = {
            "no_unbounded_self_modification",
            "no_uncontrolled_goal_proliferation",
            "memory_is_reversible",
            "execution_is_traceable",
        }

        self.history: List[Dict[str, Any]] = []

    # -------------------------
    # Identity Snapshot
    # -------------------------
    def snapshot(self) -> Dict[str, Any]:
        return {
            "identity": copy.deepcopy(self.identity),
            "invariants": list(self.invariants),
            "timestamp": time.time()
        }

    # -------------------------
    # Drift Detection
    # -------------------------
    def detect_drift(self, system_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compares system behavior against identity constraints.
        """

        drift_score = 0.0
        violations = []

        # Example checks (expandable)
        if system_state.get("mode") not in self.identity["allowed_modes"]:
            drift_score += 0.5
            violations.append("invalid_mode")

        if system_state.get("error_rate", 0) > 0.5:
            drift_score += 0.3
            violations.append("high_error_rate_drift")

        if system_state.get("goal_spawn_rate", 0) > 10:
            drift_score += 0.4
            violations.append("goal_explosion_risk")

        report = {
            "drift_score": drift_score,
            "violations": violations,
            "timestamp": time.time()
        }

        self.history.append(report)

        self.orchestrator._log("identity_drift_check", report)

        return report

    # -------------------------
    # Constraint Enforcement
    # -------------------------
    def enforce(self, meta_controller):
        """
        Applies identity constraints to system behaviour.
        """

        latest = self.history[-1] if self.history else None

        if not latest:
            return

        drift = latest.get("drift_score", 0)

        if drift > 0.7:
            # Hard safety clamp
            meta_controller.mode = "repair"
            meta_controller.system_pressure["error_rate"] += 0.2

            self.orchestrator._log("identity_enforcement_triggered", {
                "action": "forced_repair_mode"
            })

        elif drift > 0.4:
            # Soft correction
            meta_controller.mode = "balanced"

            self.orchestrator._log("identity_soft_correction", {
                "action": "mode_normalization"
            })

    # -------------------------
    # Identity Evolution (controlled)
    # -------------------------
    def evolve(self, proposal: Dict[str, Any]) -> bool:
        """
        Controlled identity update mechanism.

        Only allows evolution if:
        - does not violate invariants
        - maintains system coherence
        """

        proposed_principles = proposal.get("principles", [])

        if "no_unbounded_self_modification" in self.invariants:
            # restrict radical changes
            if len(proposed_principles) > 10:
                return False

        self.identity["principles"] = proposed_principles

        self.orchestrator._log("identity_evolved", {
            "new_principles": proposed_principles
        })

        return True
