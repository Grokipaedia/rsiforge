# cognition_compression_layer.py

from typing import Dict, Any, List, Set, Tuple
import time
import hashlib


class CompressedNode:
    """
    Represents a compressed abstraction of multiple memory or execution nodes.
    """

    def __init__(self, summary: str, source_ids: List[str]):
        self.id = hashlib.md5(summary.encode()).hexdigest()
        self.summary = summary
        self.source_ids = source_ids
        self.created_at = time.time()


class CognitionCompressionLayer:
    """
    Reduces cognitive entropy across RSIForge.

    Responsibilities:
    - merge redundant memory nodes
    - compress execution histories
    - abstract tool chains into reusable patterns
    - stabilize attention pressure
    - reduce graph explosion
    """

    def __init__(self, orchestrator, memory_graph, tool_chainer):
        self.orchestrator = orchestrator
        self.memory = memory_graph
        self.tool_chainer = tool_chainer

        self.compressed_nodes: Dict[str, CompressedNode] = {}

    # -------------------------
    # Memory Compression
    # -------------------------
    def compress_memory(self):
        """
        Merges similar memory nodes into higher-order abstractions.
        """

        seen_signatures: Dict[str, List[str]] = {}

        for node_id, node in self.memory.nodes.items():

            signature = self._signature(node)

            seen_signatures.setdefault(signature, []).append(node_id)

        for sig, node_ids in seen_signatures.items():

            if len(node_ids) < 3:
                continue  # not enough redundancy

            summary = self._summarise_nodes(node_ids)

            compressed = CompressedNode(summary, node_ids)

            self.compressed_nodes[compressed.id] = compressed

            self.orchestrator._log("memory_compressed", {
                "compressed_id": compressed.id,
                "source_count": len(node_ids)
            })

    # -------------------------
    # Execution Trace Compression
    # -------------------------
    def compress_execution_chains(self):
        """
        Converts repeated tool chains into reusable abstractions.
        """

        pattern_map: Dict[str, List[str]] = {}

        for chain_id, chain in self.tool_chainer.active_chains.items():

            pattern = tuple(step.tool_name for step in chain.steps)

            pattern_map.setdefault(pattern, []).append(chain_id)

        for pattern, chains in pattern_map.items():

            if len(chains) < 2:
                continue

            summary = f"Reusable workflow: {' -> '.join(pattern)}"

            compressed = CompressedNode(summary, chains)

            self.compressed_nodes[compressed.id] = compressed

            self.orchestrator._log("chain_compressed", {
                "compressed_id": compressed.id,
                "pattern": pattern
            })

    # -------------------------
    # Signature Function
    # -------------------------
    def _signature(self, node: Any) -> str:
        """
        Creates lightweight similarity signature for clustering.
        """

        content = str(getattr(node, "content", ""))[:100]
        tags = sorted(list(getattr(node, "tags", [])))

        raw = content + "|" + ",".join(tags)

        return hashlib.md5(raw.encode()).hexdigest()

    # -------------------------
    # Node Summarisation
    # -------------------------
    def _summarise_nodes(self, node_ids: List[str]) -> str:
        """
        Produces a compressed representation of multiple nodes.
        """

        samples = []

        for nid in node_ids[:5]:
            node = self.memory.nodes.get(nid)
            if node:
                samples.append(str(getattr(node, "content", ""))[:80])

        return " | ".join(samples)

    # -------------------------
    # Global Compression Cycle
    # -------------------------
    def run(self):
        """
        Runs full cognition compression cycle.
        """

        self.compress_memory()
        self.compress_execution_chains()

        self.orchestrator._log("compression_cycle_complete", {
            "compressed_nodes": len(self.compressed_nodes)
        })

    # -------------------------
    # Retrieval from compressed space
    # -------------------------
    def query_compressed(self, query: str) -> List[CompressedNode]:
        """
        Retrieves relevant compressed abstractions.
        """

        results = []

        for node in self.compressed_nodes.values():
            if query.lower() in node.summary.lower():
                results.append(node)

        return results
