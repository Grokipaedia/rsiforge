# multi_agent_truth_decision_engine.py

from typing import Dict, Any, List
import time
import uuid


class MultiAgentTruthDecisionEngine:
    """
    Converts multi-agent reasoning into evaluated system-level decisions.
    """

    def __init__(self, truth_engine, mutation_engine, compiler, orchestrator):
        self.truth_engine = truth_engine
        self.mutation_engine = mutation_engine
        self.compiler = compiler
        self.orchestrator = orchestrator

    # -------------------------
    # Step 1: Collect proposals
    # -------------------------
    def collect_proposals(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Replace narrative agents with structured outputs.
        """

        sigma = self._sigma(context)
        delta = self._delta(context)
        phi = self._phi([sigma, delta])

        return [sigma, delta, phi]

    # -------------------------
    # SIGMA: conservative optimizer
    # -------------------------
    def _sigma(self, context):
        return {
            "id": str(uuid.uuid4()),
            "target": "stability_system",
            "change": {"stability_bias": +0.05},
            "expected_gain": 0.05,
            "risk": 0.1,
            "rationale": "Increase system stability under current load"
        }

    # -------------------------
    # DELTA: exploration generator
    # -------------------------
    def _delta(self, context):
        return {
            "id": str(uuid.uuid4()),
            "target": "tool_chaining_planner",
            "change": {"parallelism_factor": +1},
            "expected_gain": 0.12,
            "risk": 0.3,
            "rationale": "Increase exploration via parallel execution paths"
        }

    # -------------------------
    # PHI: synthesis layer
    # -------------------------
    def _phi(self, inputs: List[Dict[str, Any]]):
        best = max(inputs, key=lambda x: x["expected_gain"] - x["risk"])

        return {
            "id": str(uuid.uuid4()),
            "target": best["target"],
            "change": best["change"],
            "expected_gain": best["expected_gain"],
            "risk": best["risk"],
            "rationale": "Synthesized best tradeoff between SIGMA and DELTA"
        }

    # -------------------------
    # Step 2: Evaluate proposals
    # -------------------------
    def evaluate(self, proposals: List[Dict[str, Any]]):
        """
        Run truth metric evaluation on each proposal.
        """

        scored = []

        for p in proposals:
            score = p["expected_gain"] - p["risk"]

            scored.append({
                **p,
                "score": score
            })

        return sorted(scored, key=lambda x: x["score"], reverse=True)

    # -------------------------
    # Step 3: Execute best proposal
    # -------------------------
    def execute_best(self, context: Dict[str, Any]):
        """
        Selects and executes the highest truth-scored proposal.
        """

        proposals = self.collect_proposals(context)
        ranked = self.evaluate(proposals)

        best = ranked[0]

        self.orchestrator._log("multi_agent_decision_selected", best)

        result = self.compiler.run_cycle(
            system_state=context,
            proposal=best
        )

        return result
