# kernel_unification.py

from typing import Dict, Any, List
import time


class KernelUnification:
    """
    Unified cognitive execution kernel for RSIForge.

    Replaces distributed control loops with a single deterministic cycle:

        perceive → attend → plan → schedule → execute → reflect → learn → evolve

    This is the top-level runtime.
    """

    def __init__(
        self,
        orchestrator,
        meta_controller,
        attention_router,
        memory_graph,
        goal_planner,
        scheduler,
        execution_graph,
        swarm_runtime,
        reflection_engine,
        value_model,
        goal_emergence_engine,
        long_horizon_planner,
        identity_kernel,
        self_mod_guard
    ):
        self.orchestrator = orchestrator

        self.meta = meta_controller
        self.attention = attention_router
        self.memory = memory_graph
        self.goal_planner = goal_planner
        self.scheduler = scheduler
        self.graph = execution_graph
        self.swarm = swarm_runtime
        self.reflection = reflection_engine
        self.value = value_model
        self.goal_emergence = goal_emergence_engine
        self.horizon = long_horizon_planner
        self.identity = identity_kernel
        self.guard = self_mod_guard

        self.cycle_count = 0
        self.last_results = []

    # -------------------------
    # SINGLE UNIFIED CYCLE
    # -------------------------
    def tick(self, external_goals: List[Dict[str, Any]] = None):
        """
        The entire cognitive system runs inside this single function.
        """

        self.cycle_count += 1

        # -------------------------
        # 1. META CONTROL (system state)
        # -------------------------
        self.meta.tick()

        # -------------------------
        # 2. LONG HORIZON GOALS
        # -------------------------
        long_goals = self.horizon.get_active_goals()

        # -------------------------
        # 3. GOAL EMERGENCE (internal generation)
        # -------------------------
        emergent_goals = self.goal_emergence.generate_goals()

        # -------------------------
        # 4. MERGE ALL GOALS
        # -------------------------
        all_goals = (external_goals or []) + long_goals + emergent_goals

        # -------------------------
        # 5. ATTENTION FILTERING
        # -------------------------
        focused_goals = []
        for g in all_goals:
            tags = g.get("payload", {}).get("tags", [])
            enriched = self.attention.focus_memory(tags)
            g["memory_context"] = enriched
            focused_goals.append(g)

        # -------------------------
        # 6. PLANNING
        # -------------------------
        plans = [self.goal_planner.plan(g) for g in focused_goals]

        # -------------------------
        # 7. SCHEDULING
        # -------------------------
        for plan in plans:
            self.scheduler.ingest_plan(plan)

        # -------------------------
        # 8. EXECUTION GRAPH BUILD
        # -------------------------
        all_tasks = []
        for plan in plans:
            for t in plan.tasks:
                all_tasks.append(t.to_dict())

        self.graph.build(all_tasks)

        ready_nodes = self.graph.get_ready_nodes()

        # -------------------------
        # 9. EXECUTION (SWARM)
        # -------------------------
        tasks = [n.task for n in ready_nodes]
        results = self.swarm.run_parallel(
            [self.swarm_runtime.SwarmTask(t["module"], t["payload"]) for t in tasks]
        )

        self.last_results = results

        # mark graph completion
        for node, result in zip(ready_nodes, results):
            self.graph.mark_complete(node.node_id, result.output)

        # -------------------------
        # 10. VALUE EVALUATION
        # -------------------------
        for r in results:
            self.value.evaluate({
                "success": r.success,
                "output": r.output,
                "latency": r.latency,
                "error": r.error
            })

        self.value.adjust_weights()

        # -------------------------
        # 11. REFLECTION
        # -------------------------
        self.reflection.reflect({
            "tasks": tasks,
            "results": results,
            "graph": self.graph.snapshot()
        })

        # -------------------------
        # 12. LONG HORIZON UPDATE
        # -------------------------
        self.horizon.tick([r.__dict__ for r in results])
        self.horizon.prune_completed()

        # -------------------------
        # 13. IDENTITY + SAFETY ENFORCEMENT
        # -------------------------
        system_state = {
            "mode": self.meta.mode,
            "error_rate": self.meta.system_pressure.get("error_rate", 0),
            "queue_depth": len(self.scheduler.queue)
        }

        drift = self.identity.detect_drift(system_state)
        self.identity.enforce(self.meta)

        # -------------------------
        # 14. SELF MODIFICATION SAFETY CHECK
        # -------------------------
        self.guard.audit()

        # -------------------------
        # LOG CYCLE COMPLETE
        # -------------------------
        self.orchestrator._log("kernel_cycle_complete", {
            "cycle": self.cycle_count,
            "tasks": len(tasks),
            "results": len(results),
            "drift": drift.get("drift_score", 0)
        })

        return {
            "cycle": self.cycle_count,
            "results": results,
            "drift": drift
        }
