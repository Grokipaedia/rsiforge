# global_execution_optimizer.py

from typing import Dict, Any, List
import time
import uuid


class ExecutionPlan:
    """
    A globally optimized execution unit (across kernels + tools).
    """

    def __init__(self, chain_id: str, priority: float, estimated_cost: float):
        self.id = str(uuid.uuid4())
        self.chain_id = chain_id
        self.priority = priority
        self.estimated_cost = estimated_cost
        self.assigned_kernel = None
        self.timestamp = time.time()


class GlobalExecutionOptimizer:
    """
    System-wide optimizer for all execution activity.

    Responsibilities:
    - distribute tool chains across swarm kernels
    - balance load vs reward
    - prioritise execution queues
    - throttle or accelerate system throughput
    - maximise global value per compute unit
    """

    def __init__(self, orchestrator, swarm_kernel, tool_chainer, value_model):
        self.orchestrator = orchestrator
        self.swarm = swarm_kernel
        self.tool_chainer = tool_chainer
        self.value_model = value_model

        self.execution_queue: List[ExecutionPlan] = []
        self.history: List[Dict[str, Any]] = []

    # -------------------------
    # Plan Ingestion
    # -------------------------
    def ingest_chain(self, chain_id: str, priority: float = 1.0):
        """
        Converts a tool chain into a globally optimised execution unit.
        """

        chain = self.tool_chainer.active_chains.get(chain_id)
        if not chain:
            return None

        estimated_cost = len(chain.steps) * 0.5  # heuristic cost model

        plan = ExecutionPlan(chain_id, priority, estimated_cost)

        self.execution_queue.append(plan)

        self.orchestrator._log("execution_plan_ingested", {
            "chain_id": chain_id,
            "priority": priority,
            "cost": estimated_cost
        })

        return plan

    # -------------------------
    # Kernel Selection Strategy
    # -------------------------
    def _select_kernel(self, plan: ExecutionPlan) -> str:
        """
        Assigns best swarm kernel for execution.
        """

        # simple heuristic: lowest load wins + priority boost
        best_kernel = None
        best_score = float("-inf")

        for kernel_id, node in self.swarm.nodes.items():

            load_penalty = node.load
            score = plan.priority - load_penalty - plan.estimated_cost * 0.1

            if score > best_score:
                best_score = score
                best_kernel = kernel_id

        return best_kernel

    # -------------------------
    # Optimization Cycle
    # -------------------------
    def optimise(self):
        """
        Main global scheduling cycle.
        """

        scheduled = []

        for plan in sorted(self.execution_queue, key=lambda p: p.priority, reverse=True):

            kernel_id = self._select_kernel(plan)

            plan.assigned_kernel = kernel_id

            scheduled.append(plan)

            self.orchestrator._log("execution_plan_assigned", {
                "plan_id": plan.id,
                "chain_id": plan.chain_id,
                "kernel": kernel_id
            })

        self.execution_queue = []

        return scheduled

    # -------------------------
    # Dispatch Execution
    # -------------------------
    def dispatch(self, scheduled: List[ExecutionPlan]):
        """
        Sends execution plans into swarm + tool execution pipeline.
        """

        results = []

        for plan in scheduled:

            chain_results = self.tool_chainer.execute_chain(
                chain_id=plan.chain_id,
                tool_layer=self.orchestrator.external_tools,
                kernel_id=plan.assigned_kernel
            )

            reward = self.value_model.evaluate({
                "success": all(chain_results),
                "output": chain_results,
                "memory_written": True
            })

            self.history.append({
                "plan_id": plan.id,
                "chain_id": plan.chain_id,
                "kernel": plan.assigned_kernel,
                "reward": reward,
                "timestamp": time.time()
            })

            self.orchestrator._log("execution_plan_completed", {
                "plan_id": plan.id,
                "reward": reward
            })

            results.append(chain_results)

        return results

    # -------------------------
    # System Efficiency Report
    # -------------------------
    def report(self) -> Dict[str, Any]:
        """
        Provides global execution efficiency metrics.
        """

        if not self.history:
            return {}

        avg_reward = sum(h["reward"] for h in self.history) / len(self.history)

        report = {
            "total_executions": len(self.history),
            "average_reward": avg_reward,
            "queue_size": len(self.execution_queue)
        }

        self.orchestrator._log("global_execution_report", report)

        return report
