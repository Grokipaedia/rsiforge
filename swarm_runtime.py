# swarm_runtime.py

from typing import Dict, Any, List, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class SwarmTask:
    """
    Represents a unit of work dispatched to the swarm.
    """
    def __init__(self, module_name: str, payload: Dict[str, Any]):
        self.module_name = module_name
        self.payload = payload


class SwarmResult:
    def __init__(self, module_name: str, output: Any, latency: float, success: bool, error: str = None):
        self.module_name = module_name
        self.output = output
        self.latency = latency
        self.success = success
        self.error = error


class SwarmRuntime:
    """
    Executes multiple Forge modules in parallel or sequence.
    Adds:
    - parallel dispatch
    - result aggregation
    - failure isolation
    - simple scheduling layer
    """

    def __init__(self, orchestrator, max_workers: int = 8):
        self.orchestrator = orchestrator
        self.max_workers = max_workers

    # -------------------------
    # Parallel Execution
    # -------------------------
    def run_parallel(self, tasks: List[SwarmTask]) -> List[SwarmResult]:
        results: List[SwarmResult] = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_map = {
                executor.submit(self._execute_task, task): task
                for task in tasks
            }

            for future in as_completed(future_map):
                results.append(future.result())

        return results

    # -------------------------
    # Sequential Execution
    # -------------------------
    def run_sequential(self, tasks: List[SwarmTask]) -> List[SwarmResult]:
        results = []
        for task in tasks:
            results.append(self._execute_task(task))
        return results

    # -------------------------
    # Core Execution Wrapper
    # -------------------------
    def _execute_task(self, task: SwarmTask) -> SwarmResult:
        start = time.time()

        try:
            output = self.orchestrator.run(
                task.module_name,
                task.payload
            )

            return SwarmResult(
                module_name=task.module_name,
                output=output,
                latency=time.time() - start,
                success=True
            )

        except Exception as e:
            return SwarmResult(
                module_name=task.module_name,
                output=None,
                latency=time.time() - start,
                success=False,
                error=str(e)
            )

    # -------------------------
    # Fan-out Pattern (one input → many modules)
    # -------------------------
    def broadcast(self, module_names: List[str], payload: Dict[str, Any]) -> List[SwarmResult]:
        tasks = [SwarmTask(name, payload) for name in module_names]
        return self.run_parallel(tasks)

    # -------------------------
    # Reduce Pattern (merge outputs)
    # -------------------------
    def reduce(self, results: List[SwarmResult], reducer: Callable) -> Any:
        """
        Takes swarm outputs and reduces them into a single result.
        """
        valid_outputs = [r.output for r in results if r.success]
        return reducer(valid_outputs)
