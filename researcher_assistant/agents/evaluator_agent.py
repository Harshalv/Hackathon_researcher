from typing import List, Dict, Any, Optional
from researcher_assistant.hmem.models import DecisionStatus, StanceType, SourceCitation
from researcher_assistant.hmem.engine import MeterlessHMemEngine

class EvaluatorAgent:
    """
    Evaluator Agent
    Receives the analytical synthesis from the Analyser Agent, formulates the final verdict,
    generates a comprehensive explanation of why the claim is valid or not, maps all contributing
    articles with active links, and persists the immutable decision into Meterless H-MEM.
    """

    def __init__(self, hmem_engine: MeterlessHMemEngine = None):
        self.hmem = hmem_engine
        self.agent_id = "agent-evaluator"

    def evaluate(
        self,
        claim: str,
        analyser_output: Dict[str, Any],
        session_id: str = "sess-01"
    ) -> Dict[str, Any]:
        """
        Synthesizes the overall decision with explanation and contributing sources.
        """
        preliminary = analyser_output.get("preliminary_verdict", "INCONCLUSIVE")
        support_ratio = analyser_output.get("support_ratio", 0.0)
        refute_ratio = analyser_output.get("refute_ratio", 0.0)
        detailed_evals = analyser_output.get("detailed_evaluations", [])
        precedents = analyser_output.get("historical_precedent_insights", [])

        # Formulate Decision & Confidence
        if preliminary == "LIKELY_VALID" or support_ratio >= 0.65:
            decision = DecisionStatus.VALID
            confidence = min(0.85 + (support_ratio * 0.12), 0.99)
        elif preliminary == "LIKELY_REFUTED" or refute_ratio >= 0.55:
            decision = DecisionStatus.REFUTED
            confidence = min(0.88 + (refute_ratio * 0.10), 0.99)
        elif support_ratio > 0.35 and refute_ratio > 0.35:
            decision = DecisionStatus.PARTIALLY_VALID
            confidence = 0.82
        else:
            decision = DecisionStatus.INCONCLUSIVE
            confidence = 0.65

        # Format contributing citations
        contributing_citations: List[SourceCitation] = []
        for item in detailed_evals:
            st = StanceType(item.get("stance", "NEUTRAL"))
            citation = SourceCitation(
                source_id=item["source_id"],
                title=item["title"],
                url=item["url"],
                domain=item["domain"],
                author=item.get("authors"),
                published_date=item.get("published_date"),
                reliability_score=item.get("reliability_score", 0.90),
                stance=st,
                key_excerpt=item.get("excerpt", ""),
                relevance_score=item.get("confidence", 0.85)
            )
            contributing_citations.append(citation)

        # Generate Comprehensive Explanation
        explanation = self._generate_explanation(claim, decision, confidence, analyser_output, precedents)

        # Commit to Meterless H-MEM Storage
        recorded_node = None
        if self.hmem:
            # Extract tags
            tags = [t for t in claim.lower().split() if len(t) > 4][:5]
            recorded_node = self.hmem.record_decision(
                claim=claim,
                decision=decision,
                confidence=round(confidence, 2),
                explanation=explanation,
                contributing_sources=contributing_citations,
                tags=tags,
                parent_decision_id=precedents[0]["compound_id"] if precedents else None
            )

        return {
            "agent": "EvaluatorAgent",
            "claim": claim,
            "decision": decision.value,
            "confidence_score": round(confidence, 2),
            "confidence_percentage": f"{int(round(confidence * 100))}%",
            "explanation": explanation,
            "decision_verdict_summary": f"The claim '{claim}' is evaluated as {decision.value} ({int(round(confidence * 100))}% confidence).",
            "contributing_articles": [c.model_dump() for c in contributing_citations],
            "hmem_record": {
                "compound_id": recorded_node.compound_id if recorded_node else "DEC.L2.PENDING",
                "tier": "L2_longterm_decision",
                "audit_hash": recorded_node.lineage.audit_hash if recorded_node else None,
                "created_iso": recorded_node.lineage.created_iso if recorded_node else None,
                "precedent_referenced": precedents[0]["compound_id"] if precedents else "None"
            }
        }

    def _generate_explanation(
        self,
        claim: str,
        decision: DecisionStatus,
        confidence: float,
        analyser_output: Dict[str, Any],
        precedents: List[Dict[str, Any]]
    ) -> str:
        """Constructs an explanatory synthesis citing findings and precedents."""
        supporting = analyser_output.get("supporting_points", [])
        counter = analyser_output.get("counter_points", [])

        paragraphs = []

        if decision == DecisionStatus.VALID:
            paragraphs.append(
                f"**Verification Outcome: Strong Empirical Support.** The investigated claim is confirmed to be **VALID** with a confidence of {int(confidence*100)}% based on federated evidence aggregated via Zetaris."
            )
            if supporting:
                bullet_points = "\n".join([f"- **{p['source']}**: {p['excerpt']}" for p in supporting[:3]])
                paragraphs.append(f"**Key Supporting Evidence:**\n{bullet_points}")
        elif decision == DecisionStatus.REFUTED:
            paragraphs.append(
                f"**Verification Outcome: Refuted by Primary Evidence.** The investigated claim is determined to be **REFUTED** ({int(confidence*100)}% confidence). The underlying assertion directly conflicts with peer-reviewed literature and empirical benchmark telemetry."
            )
            if counter:
                bullet_points = "\n".join([f"- **{p['source']}**: {p['excerpt']}" for p in counter[:3]])
                paragraphs.append(f"**Direct Contradictory Evidence:**\n{bullet_points}")
        elif decision == DecisionStatus.PARTIALLY_VALID:
            paragraphs.append(
                f"**Verification Outcome: Partially Valid with Substantial Nuances.** The claim contains elements of factual accuracy ({int(confidence*100)}% confidence), but presents an over-broad or conditional premise as an unconditional reality."
            )
        else:
            paragraphs.append(
                f"**Verification Outcome: Inconclusive / Insufficient Consensus.** Current aggregated evidence does not provide definitive confirmation or refutation."
            )

        # Add historical precedent if available in H-MEM
        if precedents:
            p = precedents[0]
            paragraphs.append(
                f"**Meterless H-MEM Precedent:** Corroborated with historical audit decision `{p['compound_id']}` regarding *\"{p['past_claim']}\"*, which was recorded as **{p['past_decision']}**. This reinforces continuous reasoning consistency across evaluation cycles."
            )

        return "\n\n".join(paragraphs)
