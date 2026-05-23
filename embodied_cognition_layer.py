# embodied_cognition_layer.py

from typing import Dict, Any, Callable, List, Optional
import time
import uuid


class EmbodiedAction:
    """
    Represents an action executed in an external environment.
    """

    def __init__(self, action_type: str, payload: Dict[str, Any]):
        self.id = str(uuid.uuid4())
        self.action_type = action_type
        self.payload = payload
        self.timestamp = time.time()
        self.result = None
        self.success = None


class EmbodiedCognitionLayer:
    """
    Bridges internal cognition with external world interaction.

    Responsibilities:
    - sensor ingestion
    - motor/action execution
    - grounding feedback
    - reality alignment tracking
    """

    def __init__(self, orchestrator, external_tool_layer, memory, value_model):
        self.orchestrator = orchestrator
        self.tools = external_tool_layer
        self.memory = memory
        self.value = value_model

        self.sensors: Dict[str, Callable] = {}
        self.effectors: Dict[str, Callable] = {}

        self.active_actions: Dict[str, EmbodiedAction] = {}

    # -------------------------
    # Sensor Registration
    # -------------------------
    def register_sensor(self, name: str, fn: Callable):
        self.sensors[name] = fn

        self.orchestrator._log("sensor_registered", {
            "sensor": name
        })

    # -------------------------
    # Effector Registration
    # -------------------------
    def register_effector(self, name: str, fn: Callable):
        self.effectors[name] = fn

        self.orchestrator._log("effector_registered", {
            "effector": name
        })

    # -------------------------
    # Perception (Grounding Input)
    # -------------------------
    def sense(self) -> Dict[str, Any]:
        """
        Pulls state from external environment.
        """

        perception = {}

        for name, sensor in self.sensors.items():
            try:
                perception[name] = sensor()
            except Exception as e:
                perception[name] = {"error": str(e)}

        self.orchestrator._log("embodied_sense_tick", {
            "sensors": list(perception.keys())
        })

        return perception

    # -------------------------
    # Action Execution (Motor Output)
    # -------------------------
    def act(self, action_type: str, payload: Dict[str, Any]) -> EmbodiedAction:
        """
        Executes a real-world action via tools or effectors.
        """

        action = EmbodiedAction(action_type, payload)

        self.active_actions[action.id] = action

        try:
            if action_type in self.effectors:
                result = self.effectors[action_type](payload)

            else:
                # fallback to external tool layer
                result = self.tools.execute(action_type, payload)

            action.result = result
            action.success = True

        except Exception as e:
            action.result = None
            action.success = False

        # -------------------------
        # store grounding memory
        # -------------------------
        self.memory.write_node("embodiment", {
            "action": action_type,
            "payload": payload,
            "success": action.success,
            "result": action.result
        })

        self.orchestrator._log("embodied_action_executed", {
            "action_type": action_type,
            "success": action.success
        })

        return action

    # -------------------------
    # Feedback Loop (Reality Alignment)
    # -------------------------
    def evaluate_alignment(self, predicted: Dict[str, Any], actual: Dict[str, Any]) -> float:
        """
        Measures mismatch between expected and real outcomes.
        """

        score = 1.0

        for k in predicted:
            if predicted[k] != actual.get(k):
                score -= 0.2

        score = max(0.0, score)

        self.value.evaluate({
            "alignment_score": score,
            "predicted": predicted,
            "actual": actual
        })

        self.orchestrator._log("embodied_alignment_evaluated", {
            "score": score
        })

        return score

    # -------------------------
    # Action History Query
    # -------------------------
    def recent_actions(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        Returns most recent embodied interactions.
        """

        actions = list(self.active_actions.values())[-n:]

        return [
            {
                "id": a.id,
                "type": a.action_type,
                "success": a.success,
                "timestamp": a.timestamp
            }
            for a in actions
        ]
