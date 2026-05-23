# tool_chaining_planner.py

from typing import Dict, Any, List, Optional
import uuid
import time


class ToolStep:
    """
    A single step in a tool execution chain.
    """

    def __init__(
        self,
        tool_name: str,
        input_map: Dict[str, Any],
        depends_on: Optional[List[str]] = None
    ):
        self.id = str(uuid.uuid4())
        self.tool_name = tool_name
        self.input_map = input_map
        self.depends_on = depends_on or []
        self.completed = False
        self.output = None


class ToolChain:
    """
    A sequence of tool steps forming a reasoning pipeline.
    """

    def __init__(self, goal_id: str, description: str):
        self.id = str(uuid.uuid4())
        self.goal_id = goal_id
        self.description = description
        self.steps: List[ToolStep] = []
        self.created_at = time.time()

    def add_step(self, step: ToolStep):
        self.steps.append(step)


class ToolChainingPlanner:
    """
    Converts goals into multi-step tool execution strategies.

    This is where:
    - reasoning becomes procedural
    - tools become composable
    - execution becomes structured cognition
    """

    def __init__(self, orchestrator, tool_layer):
        self.orchestrator = orchestrator
        self.tools = tool_layer

        self.active_chains: Dict[str, ToolChain] = {}

    # -------------------------
    # Chain Generation
    # -------------------------
    def build_chain(self, goal: Dict[str, Any]) -> ToolChain:
        """
        Creates a multi-step tool execution plan from a goal.
        """

        chain = ToolChain(
            goal_id=goal.get("id", "unknown"),
            description=goal.get("objective", "")
        )

        objective = goal.get("objective", "").lower()

        # -------------------------
        # SIMPLE HEURISTIC ROUTER
        # (replace later with LLM planner)
        # -------------------------

        # Example: data retrieval pipeline
        if "search" in objective or "find" in objective:
            chain.add_step(ToolStep("search_api", {"query": objective}))
            chain.add_step(ToolStep("summarize", {"input": "search_api.output"}))

        # Example: analysis pipeline
        elif "analyze" in objective:
            chain.add_step(ToolStep("fetch_data", {"source": objective}))
            chain.add_step(ToolStep("analyze_data", {"input": "fetch_data.output"}))
            chain.add_step(ToolStep("report", {"input": "analyze_data.output"}))

        # Example: generic reasoning fallback
        else:
            chain.add_step(ToolStep("reasoner", {"input": objective}))

        self.active_chains[chain.id] = chain

        self.orchestrator._log("tool_chain_created", {
            "chain_id": chain.id,
            "steps": len(chain.steps)
        })

        return chain

    # -------------------------
    # Dependency Resolution
    # -------------------------
    def resolve_inputs(self, step: ToolStep, memory: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolves dynamic inputs between steps.
        """

        resolved = {}

        for k, v in step.input_map.items():

            if isinstance(v, str) and "." in v:
                # e.g. "search_api.output"
                ref_step, field = v.split(".")
                resolved[k] = memory.get(ref_step, {}).get(field)
            else:
                resolved[k] = v

        return resolved

    # -------------------------
    # Execution Planning
    # -------------------------
    def execute_chain(self, chain_id: str, tool_layer, kernel_id: str = "global") -> List[Any]:
        """
        Executes a full tool chain step-by-step.
        """

        chain = self.active_chains.get(chain_id)
        if not chain:
            return []

        memory = {}
        results = []

        for step in chain.steps:

            inputs = self.resolve_inputs(step, memory)

            result = tool_layer.execute(
                tool_name=step.tool_name,
                payload=inputs,
                kernel_id=kernel_id
            )

            step.completed = True
            step.output = result

            memory[step.tool_name] = {
                "output": result
            }

            results.append(result)

            self.orchestrator._log("tool_chain_step_executed", {
                "chain_id": chain_id,
                "step": step.tool_name
            })

        return results

    # -------------------------
    # Chain Analysis
    # -------------------------
    def analyze_chain(self, chain_id: str) -> Dict[str, Any]:
        """
        Evaluates performance of a tool chain.
        """

        chain = self.active_chains.get(chain_id)
        if not chain:
            return {}

        success_count = sum(1 for s in chain.steps if s.completed)

        report = {
            "chain_id": chain_id,
            "steps": len(chain.steps),
            "completed": success_count,
            "efficiency": success_count / max(1, len(chain.steps))
        }

        self.orchestrator._log("tool_chain_analysis", report)

        return report
