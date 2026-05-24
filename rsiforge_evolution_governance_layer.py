# rsiforge_evolution_governance_layer.py

from typing import Dict, Any, List
import time
import uuid


class SystemVersion:
    def __init__(self, version: str, description: str):
        self.id = str(uuid.uuid4())
        self.version = version
        self.description = description
        self.timestamp = time.time()


class RSIForgeEvolutionGovernanceLayer:
    """
    Governs how RSIForge itself evolves over time.

    This is NOT part of runtime cognition.
    This is meta-governance over system evolution.
    """

    def __init__(self):
        self.current_version = "0.1.0"

        self.versions: List[SystemVersion] = []

        self.allowed_changes = {
            "add_module": True,
            "modify_evaluation": True,
            "modify_objectives": False,  # requires governance approval
            "modify_truth_axioms": False,
            "remove_epistemic_constraints": False
        }

        self.rollback_points: List[str] = []

    # -------------------------
    # Step 1: Register new version
    # -------------------------
    def register_version(self, description: str):
        version = self._increment_version()

        sv = SystemVersion(version, description)
        self.versions.append(sv)

        return sv

    # -------------------------
    # Step 2: Version increment logic
    # -------------------------
    def _increment_version(self) -> str:
        major, minor, patch = map(int, self.current_version.split("."))

        patch += 1

        self.current_version = f"{major}.{minor}.{patch}"

        return self.current_version

    # -------------------------
    # Step 3: Validate system change
    # -------------------------
    def validate_change(self, change: Dict[str, Any]) -> bool:
        """
        Ensures system evolution stays within governance rules.
        """

        change_type = change.get("type")

        if change_type not in self.allowed_changes:
            return False

        return self.allowed_changes[change_type]

    # -------------------------
    # Step 4: Create rollback checkpoint
    # -------------------------
    def create_checkpoint(self):
        """
        Marks a safe recovery state.
        """

        self.rollback_points.append(self.current_version)

        return {
            "status": "checkpoint_created",
            "version": self.current_version
        }

    # -------------------------
    # Step 5: Rollback system
    # -------------------------
    def rollback(self):
        """
        Restores previous stable version.
        """

        if not self.rollback_points:
            return {"status": "no_checkpoint_available"}

        last = self.rollback_points.pop()

        self.current_version = last

        return {
            "status": "rolled_back",
            "version": self.current_version
        }
