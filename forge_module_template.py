# forge_module_template.py

from abc import ABC, abstractmethod
from typing import Dict, Any


class ForgeModule(ABC):
    """
    Base contract for all RSIForge modules.

    Every module must:
    - accept ForgeState + input payload
    - return structured output
    - remain stateless except via ForgeState
    """

    name: str = "unnamed_module"
    version: str = "0.0.1"

    # -------------------------
    # Core Interface
    # -------------------------
    @abstractmethod
    def run(self, state, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution entry point.
        Must be implemented by all modules.
        """
        pass

    # -------------------------
    # Optional Lifecycle Hooks
    # -------------------------
    def on_register(self, state) -> None:
        """
        Called when module is registered in the orchestrator.
        """
        pass

    def on_unregister(self, state) -> None:
        """
        Called when module is removed from orchestrator.
        """
        pass

    def on_event(self, state, event: Dict[str, Any]) -> None:
        """
        Hook for reacting to system events.
        Optional reactive behavior layer.
        """
        pass

    # -------------------------
    # Helper Wrappers
    # -------------------------
    def execute(self, state, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Safe execution wrapper around run().
        Adds structure for logging/debug hooks later.
        """
        return self.run(state, input_data)


class SimpleFunctionModule(ForgeModule):
    """
    Lightweight adapter for turning a function into a ForgeModule.
    """

    def __init__(self, func, name: str = None):
        self.func = func
        self.name = name or func.__name__

    def run(self, state, input_data: Dict[str, Any]) -> Dict[str, Any]:
        result = self.func(state, input_data)

        # Normalize output
        if isinstance(result, dict):
            return result

        return {"result": result}
