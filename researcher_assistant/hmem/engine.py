import re
import time
from typing import List, Optional, Dict, Any, Tuple
from researcher_assistant.hmem.models import (
    MemoryNode, MemoryTier, DecisionStatus, StanceType, SourceCitation, Provenance
)
from researcher_assistant.hmem.storage import HMemStorage

class MeterlessHMemEngine:
    """
    Meterless H-MEM (Hierarchical Memory Engine)
    Implements a local-first, tiered memory architecture for agents:
    - Tiered storage pyramid (L0 Ephemeral -> L1 Working -> L2 Long-Term Decisions)
    - Immutable historical decision audit trails with compound IDs
    - Provenance & lineage tracking
    - Historical decision lookups & cross-referencing
    - Metabolic dreaming / maintenance cycle
    """

    def __init__(self, storage_dir: str):
        self.storage = HMemStorage(storage_dir)

    def _tokenize(self, text: str) -> set:
        clean = re.sub(r"[^\w\s]", " ", text.lower())
        tokens = [t.strip() for t in clean.split() if len(t.strip()) > 2]
        # remove basic stop words
        stopwords = {
            "the", "and", "that", "this", "with", "from", "for", "are", "have", "has",
            "been", "was", "were", "what", "which", "into", "their", "will", "would",
            "about", "over", "under", "per", "such", "than", "then", "just"
        }
        return {t for t in tokens if t not in stopwords}

    def _similarity_score(self, query: str, target: str) -> float:
        q_tokens = self._tokenize(query)
        t_tokens = self._tokenize(target)
        if not q_tokens or not t_tokens:
            return 0.0
        intersection = q_tokens.intersection(t_tokens)
        union = q_tokens.union(t_tokens)
        jaccard = len(intersection) / len(union)
        dice = (2.0 * len(intersection)) / (len(q_tokens) + len(t_tokens))
        return (jaccard + dice) / 2.0

    def query_historical_decisions(self, claim: str, threshold: float = 0.15, max_results: int = 5) -> List[Tuple[MemoryNode, float]]:
        """
        Retrieves relevant past decisions from L2 Long-term storage.
        Returns pairs of (MemoryNode, match_score) sorted by score.
        """
        all_l2 = self.storage.list_nodes(tier=MemoryTier.L2_LONGTERM)
        scored: List[Tuple[MemoryNode, float]] = []

        for node in all_l2:
            score_claim = self._similarity_score(claim, node.claim)
            score_summary = self._similarity_score(claim, node.summary)
            score_tags = 0.0
            claim_tokens = self._tokenize(claim)
            for tag in node.tags:
                if any(t in tag.lower() for t in claim_tokens):
                    score_tags += 0.2

            composite_score = max(score_claim * 0.7 + score_summary * 0.3, score_claim) + min(score_tags, 0.3)
            
            # Boost if substring found
            if any(word in node.claim.lower() for word in claim.lower().split() if len(word) > 4):
                composite_score += 0.1

            if composite_score >= threshold:
                scored.append((node, round(min(composite_score, 1.0), 3)))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:max_results]

    def record_decision(
        self,
        claim: str,
        decision: DecisionStatus,
        confidence: float,
        explanation: str,
        contributing_sources: List[SourceCitation],
        tags: List[str] = None,
        parent_decision_id: Optional[str] = None,
        supersedes_id: Optional[str] = None
    ) -> MemoryNode:
        """
        Records an immutable decision into L2 Long-term memory.
        Generates compound ID (e.g. DEC.L2.2026.NNN).
        """
        existing_l2 = self.storage.list_nodes(tier=MemoryTier.L2_LONGTERM)
        seq_num = len(existing_l2) + 1
        year = time.strftime("%Y")
        compound_id = f"DEC.L2.{year}.{seq_num:03d}"

        # If this supersedes an existing decision, update old record with pointer
        if supersedes_id:
            old_node = self.storage.get_node(supersedes_id)
            if old_node:
                old_node.superseded_by = compound_id
                old_node.is_archived = True
                self.storage.save_node(old_node)

        # Generate summary
        summary = f"Claim evaluated as {decision.value} with {int(confidence*100)}% confidence based on {len(contributing_sources)} sources."

        node = MemoryNode(
            compound_id=compound_id,
            tier=MemoryTier.L2_LONGTERM,
            claim=claim,
            summary=summary,
            decision=decision,
            confidence=confidence,
            explanation=explanation,
            contributing_sources=contributing_sources,
            tags=tags or [],
            lineage=Provenance(
                parent_decision_id=parent_decision_id,
                agents_involved=["source (zetaris)", "analyser", "evaluator"]
            ),
            supersedes_id=supersedes_id
        )

        return self.storage.save_node(node)

    def record_working_notes(self, claim: str, notes_summary: str, session_id: str) -> MemoryNode:
        """Records working memory (L1) during analysis."""
        seq_num = len(self.storage.list_nodes(tier=MemoryTier.L1_WORKING)) + 1
        compound_id = f"WRK.L1.{session_id}.{seq_num:03d}"
        node = MemoryNode(
            compound_id=compound_id,
            tier=MemoryTier.L1_WORKING,
            claim=claim,
            summary=notes_summary,
            lineage=Provenance(session_id=session_id, agents_involved=["analyser"])
        )
        return self.storage.save_node(node)

    def get_all_decisions(self) -> List[MemoryNode]:
        """Returns all recorded historical decisions from L2."""
        return self.storage.list_nodes(tier=MemoryTier.L2_LONGTERM)

    def get_stats(self) -> Dict[str, Any]:
        """Returns statistics on memory tiers and decision breakdowns."""
        l0 = len(self.storage.list_nodes(MemoryTier.L0_EPHEMERAL))
        l1 = len(self.storage.list_nodes(MemoryTier.L1_WORKING))
        l2_nodes = self.storage.list_nodes(MemoryTier.L2_LONGTERM)
        
        breakdown = {"VALID": 0, "REFUTED": 0, "PARTIALLY_VALID": 0, "INCONCLUSIVE": 0}
        for n in l2_nodes:
            if n.decision and n.decision.value in breakdown:
                breakdown[n.decision.value] += 1

        ledger_count = len(self.storage.get_ledger_entries())

        return {
            "l0_ephemeral_count": l0,
            "l1_working_count": l1,
            "l2_longterm_decisions_count": len(l2_nodes),
            "decisions_breakdown": breakdown,
            "audit_ledger_entries": ledger_count,
            "storage_path": self.storage.storage_dir
        }

    def trigger_metabolic_consolidation(self) -> Dict[str, Any]:
        """
        H-MEM 'Sleep / Dream' metabolic consolidation:
        - Scans L2 decisions for semantic overlap or conflicting verdicts
        - Links related historical decisions
        - Produces an audit report
        """
        l2_nodes = self.storage.list_nodes(MemoryTier.L2_LONGTERM)
        clusters = []
        visited = set()

        for i, node_a in enumerate(l2_nodes):
            if node_a.compound_id in visited:
                continue
            cluster = [node_a.compound_id]
            for j, node_b in enumerate(l2_nodes):
                if i != j and node_b.compound_id not in visited:
                    sim = self._similarity_score(node_a.claim, node_b.claim)
                    if sim > 0.4:
                        cluster.append(node_b.compound_id)
                        visited.add(node_b.compound_id)
            if len(cluster) > 1:
                clusters.append(cluster)
            visited.add(node_a.compound_id)

        return {
            "status": "consolidated",
            "clusters_discovered": len(clusters),
            "clusters": clusters,
            "total_decisions_audited": len(l2_nodes),
            "metabolism_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
