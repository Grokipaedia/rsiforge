# self_modification_guard.py

from typing import Dict, Any, List, Set
import time
import copy


class SelfModificationGuard:
    """
    Controls all attempts at system self-modification.

    Purpose:
    - prevent unsafe recursive self-editing
    - enforce identity + invariant constraints
    - validate system evolution proposals
    - log all structural mutation attempts
    """

    def __init__(self, orchestrator, identity_kernel):
        self.orchestrator = orchestrator
        self.identity = identity_kernel

        # Hard safety constraints (non-negotiable)
        self.hard_invariants: Set[str] = {
            "no_unbounded_self_rewrite",
            "no_removal_of_identity_kernel",
            "no_disabling_of_memory_graph",
            "no_disabling_of_attention_router",
            "no_circular_meta_modification"
        }

        self.approval_log: List[Dict[str, Any]] = []

    # -------------------------
    # Main Gate Function
    # -------------------------
    def validate_modification(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates whether a proposed system modification is safe.
        """

        risk_score = 0.0
        violations = []

        change_type = proposal.get("type")
        target = proposal.get("target")
        payload = proposal.get("payload", {})

        # -------------------------
        # Identity protection
        # -------------------------
        if target == "identity_kernel":
            risk_score += 1.0
            violations.append("identity_kernel_modification_attempt")

        # -------------------------
        # Core subsystem protection
        # -------------------------
        if target in self.hard_invariants:
            risk_score += 1.0
            violations.append("hard_invariant_violation")

        # -------------------------
        # Structural rewrite risk
        # -------------------------
        if change_type in ["delete", "disable", "replace_core_loop"]:
            risk_score += 0.7
            violations.append("core_structural_change")

        # -------------------------
        # Recursive instability detection
        # -------------------------
        if payload.get("affects_self_modification_guard"):
            risk_score += 1.0
            violations.append("recursive_guard_modification")

        # -------------------------
        # Evolution allowance heuristic
        # -------------------------
        allowed = risk_score < 0.5

        decision = {
            "allowed": allowed,
            "risk_score": risk_score,
            "violations": violations,
            "timestamp": time.time(),
            "proposal": copy.deepcopy(proposal)
        }

        self.approval_log.append(decision)

        self.orchestrator._log("self_modification_check", decision)

        return decision

    # -------------------------
    # Safe Evolution Path
    # -------------------------
    def safe_apply(self, proposal: Dict[str, Any], apply_fn):
        """
        Applies modification only if validated safe.
        """

        decision = self.validate_modification(proposal)

        if not decision["allowed"]:
            self.orchestrator._log("self_modification_blocked", decision)
            return False

        # execute approved change
        result = apply_fn(proposal)

        self.orchestrator._log("self_modification_applied", {
            "proposal": proposal,
            "result": str(result)
        })

        return True

    # -------------------------
    # Drift Monitoring
    # -------------------------
    def audit(self):
        """
        Checks whether past modifications are causing instability.
        """

        recent = self.approval_log[-20:]

        risk_trend = sum(d["risk_score"] for d in recent) / max(1, len(recent))

        if risk_trend > 0.6:
            self.orchestrator._log("self_modification_risk_warning", {
                "risk_trend": risk_trend
            })

        return {
            "risk_trend": risk_trend,
            "entries": len(recent)
        }
