import uuid
import time
from typing import Dict, Any, Generator, Optional
from researcher_assistant.hmem.engine import MeterlessHMemEngine
from researcher_assistant.zetaris.connector import ZetarisConnector
from researcher_assistant.agents.source_agent import SourceAgent
from researcher_assistant.agents.analyser_agent import AnalyserAgent
from researcher_assistant.agents.evaluator_agent import EvaluatorAgent

class ResearcherAssistantCoordinator:
    """
    Coordinates the 3 core agents:
    1. SourceAgent (Zetaris Data Aggregator)
    2. AnalyserAgent (Claim vs. Notes Validation)
    3. EvaluatorAgent (Final Decision, Explanation, Contributing Links, H-MEM Ingestion)
    Integrated with Meterless H-MEM to remember historical decisions.
    """

    def __init__(
        self,
        hmem_engine: MeterlessHMemEngine,
        zetaris_connector: Optional[ZetarisConnector] = None
    ):
        self.hmem = hmem_engine
        self.zetaris = zetaris_connector or ZetarisConnector()
        self.source_agent = SourceAgent(self.zetaris)
        self.analyser_agent = AnalyserAgent()
        self.evaluator_agent = EvaluatorAgent(self.hmem)

    def evaluate_claim_stream(self, claim: str) -> Generator[Dict[str, Any], None, Dict[str, Any]]:
        """
        Executes the agentic researcher workflow yielding streaming status events
        for real-time sleek UI updates.
        """
        session_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        # Step 0: Initialize
        yield {
            "type": "step",
            "step": "init",
            "agent": "Coordinator",
            "message": f"Received claim for evaluation: '{claim}'",
            "session_id": session_id,
            "timestamp": time.time()
        }

        # Step 1: Query Meterless H-MEM for past decisions
        yield {
            "type": "step",
            "step": "hmem_lookup",
            "agent": "Meterless H-MEM",
            "message": "Scanning L2 long-term memory for relevant historical decisions...",
            "session_id": session_id,
            "timestamp": time.time()
        }
        
        hist_matches = self.hmem.query_historical_decisions(claim=claim, threshold=0.15, max_results=3)
        formatted_precedents = []
        for node, score in hist_matches:
            formatted_precedents.append({
                "compound_id": node.compound_id,
                "claim": node.claim,
                "decision": node.decision.value if node.decision else "UNKNOWN",
                "similarity": score,
                "confidence": node.confidence,
                "explanation_snippet": (node.explanation[:120] + "...") if node.explanation else ""
            })

        yield {
            "type": "step",
            "step": "hmem_lookup_complete",
            "agent": "Meterless H-MEM",
            "message": f"Retrieved {len(formatted_precedents)} historical decisions from persistent H-MEM memory store.",
            "data": formatted_precedents,
            "session_id": session_id,
            "timestamp": time.time()
        }

        # Step 2: Source Agent aggregates data via Zetaris
        yield {
            "type": "step",
            "step": "source_agent_started",
            "agent": "SourceAgent (Zetaris)",
            "message": "Dispatching federated query across Zetaris enterprise data fabric & research pools...",
            "session_id": session_id,
            "timestamp": time.time()
        }

        source_output = self.source_agent.aggregate_sources(claim=claim)

        yield {
            "type": "step",
            "step": "source_agent_complete",
            "agent": "SourceAgent (Zetaris)",
            "message": f"Zetaris aggregated {source_output['sources_count']} relevant sources & observational notes across data pools.",
            "data": source_output,
            "session_id": session_id,
            "timestamp": time.time()
        }

        # Step 3: Analyser Agent analyzes the notes
        yield {
            "type": "step",
            "step": "analyser_agent_started",
            "agent": "AnalyserAgent",
            "message": "Analyzing gathered notes to check if the input claim is valid as per the notes...",
            "session_id": session_id,
            "timestamp": time.time()
        }

        analyser_output = self.analyser_agent.analyze_notes(
            claim=claim,
            source_output=source_output,
            historical_decisions=formatted_precedents
        )

        # Store intermediate working memory in H-MEM L1
        self.hmem.record_working_notes(
            claim=claim,
            notes_summary=analyser_output["analysis_summary"],
            session_id=session_id
        )

        yield {
            "type": "step",
            "step": "analyser_agent_complete",
            "agent": "AnalyserAgent",
            "message": f"Analysis complete. Preliminary stance: {analyser_output['preliminary_verdict']} (Support: {int(analyser_output['support_ratio']*100)}%, Refute: {int(analyser_output['refute_ratio']*100)}%).",
            "data": analyser_output,
            "session_id": session_id,
            "timestamp": time.time()
        }

        # Step 4: Evaluator Agent gives overall decision and links
        yield {
            "type": "step",
            "step": "evaluator_agent_started",
            "agent": "EvaluatorAgent",
            "message": "Synthesizing overall decision, explanation, and contributing article links...",
            "session_id": session_id,
            "timestamp": time.time()
        }

        evaluator_output = self.evaluator_agent.evaluate(
            claim=claim,
            analyser_output=analyser_output,
            session_id=session_id
        )

        elapsed = round(time.time() - start_time, 2)

        # Final complete payload
        final_result = {
            "type": "complete",
            "session_id": session_id,
            "elapsed_seconds": elapsed,
            "claim": claim,
            "decision": evaluator_output["decision"],
            "confidence_score": evaluator_output["confidence_score"],
            "confidence_percentage": evaluator_output["confidence_percentage"],
            "explanation": evaluator_output["explanation"],
            "contributing_articles": evaluator_output["contributing_articles"],
            "historical_precedents": formatted_precedents,
            "hmem_record": evaluator_output["hmem_record"],
            "source_data": source_output,
            "analyser_data": analyser_output
        }

        yield final_result
        return final_result

    def evaluate_claim_sync(self, claim: str) -> Dict[str, Any]:
        """Synchronous full evaluation helper."""
        last_event = None
        for event in self.evaluate_claim_stream(claim):
            if event.get("type") == "complete":
                last_event = event
        return last_event
