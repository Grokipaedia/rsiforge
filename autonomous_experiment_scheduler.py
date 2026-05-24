# autonomous_experiment_scheduler.py

from typing import Dict, Any, List
import time
import uuid
import random


class Experiment:
    """
    Represents a single controlled system experiment.
    """

    def __init__(self, config: Dict[str, Any], hypothesis: str):
        self.id = str(uuid.uuid4())
        self.config = config
        self.hypothesis = hypothesis
        self.created_at = time.time()
        self.status = "pending"
        self.result = None


class AutonomousExperimentScheduler:
    """
    Continuously generates and evaluates system experiments.

    This is the bridge between:
    - mutation proposals
    - truth metric evaluation
    - long-term system evolution tracking
    """

    def __init__(self, mutation_engine, compiler, sandbox, truth_engine, orchestrator):
        self.mutation_engine = mutation_engine
        self.compiler = compiler
        self.sandbox = sandbox
        self.truth_engine = truth_engine
        self.orchestrator = orchestrator

        self.active_experiments: List[Experiment] = []
        self.completed_experiments: List[Experiment] = []

    # -------------------------
    # Step 1: Generate experiments
    # -------------------------
    def generate_experiments(self, system_state: Dict[str, Any], n: int = 3) -> List[Experiment]:
        """
        Create candidate system variations from mutation engine.
        """

        experiments = []

        for _ in range(n):
            proposal = self.mutation_engine.generate_next_upgrade()

            experiment = Experiment(
                config=proposal,
                hypothesis=proposal.get("rationale", "unknown improvement hypothesis")
            )

            experiments.append(experiment)

        self.active_experiments.extend(experiments)

        self.orchestrator._log("experiments_generated", {
            "count": len(experiments)
        })

        return experiments

    # -------------------------
    # Step 2: Execute experiment
    # -------------------------
    def run_experiment(self, experiment: Experiment, system_state: Dict[str, Any]):
        """
        Executes a system variant in sandbox.
        """

        experiment.status = "running"

        try:
            new_version = self.compiler.run_cycle(
                system_state=system_state,
                proposal=experiment.config
            )

            results = self.sandbox.run(new_version["new_version_id"])

            evaluation = self.truth_engine.evaluate_version(
                new_version["new_version_id"],
                results
            )

            experiment.result = {
                "evaluation": evaluation,
                "success": True
            }

            experiment.status = "completed"

        except Exception as e:
            experiment.result = {
                "error": str(e),
                "success": False
            }
            experiment.status = "failed"

        self.completed_experiments.append(experiment)

        self.orchestrator._log("experiment_completed", {
            "experiment_id": experiment.id,
            "status": experiment.status
        })

    # -------------------------
    # Step 3: Continuous scheduling loop
    # -------------------------
    def run_scheduler_cycle(self, system_state: Dict[str, Any]):
        """
        Main autonomous loop.
        """

        # 1. generate new experiments
        new_experiments = self.generate_experiments(system_state)

        # 2. run each experiment
        for exp in new_experiments:
            self.run_experiment(exp, system_state)

        # 3. analyze results
        self.analyze_results()

    # -------------------------
    # Step 4: Analyze outcomes
    # -------------------------
    def analyze_results(self):
        """
        Finds best-performing experimental changes.
        """

        valid = [
            e for e in self.completed_experiments
            if e.result and e.result.get("success")
        ]

        if not valid:
            return {"status": "no_valid_experiments"}

        ranked = sorted(
            valid,
            key=lambda e: e.result["evaluation"]["mean_score"],
            reverse=True
        )

        best = ranked[0]

        self.orchestrator._log("best_experiment_found", {
            "experiment_id": best.id,
            "score": best.result["evaluation"]["mean_score"]
        })

        return best
