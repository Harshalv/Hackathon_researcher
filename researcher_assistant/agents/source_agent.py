from typing import List, Dict, Any
from researcher_assistant.zetaris.connector import ZetarisConnector

class SourceAgent:
    """
    Source Agent
    Acts as the information gatherer using Zetaris Data Fabric as a data aggregator.
    Dispatches queries across federated catalogs, databases, and research pools.
    Extracts structured notes and citations.
    """

    def __init__(self, zetaris_connector: ZetarisConnector = None):
        self.zetaris = zetaris_connector or ZetarisConnector()
        self.agent_id = "agent-source-zetaris"

    def aggregate_sources(self, claim: str) -> Dict[str, Any]:
        """
        Queries Zetaris to aggregate relevant data sources and extract research notes.
        """
        # Federated search across Zetaris data fabric
        raw_results = self.zetaris.federated_query(claim=claim, limit=4)

        aggregated_notes = []
        sources = []

        for item in raw_results:
            note_entry = {
                "source_id": item["source_id"],
                "data_pool": item["data_pool"],
                "title": item["title"],
                "url": item["url"],
                "domain": item["domain"],
                "authors": item.get("authors", "Institutional Contributor"),
                "published_date": item.get("published_date", "2024"),
                "reliability_score": item.get("reliability_score", 0.90),
                "relevance_score": item.get("relevance_score", 0.85),
                "summary": item["summary"],
                "notes": item["notes"]
            }
            aggregated_notes.append(note_entry)
            sources.append({
                "source_id": item["source_id"],
                "title": item["title"],
                "url": item["url"],
                "domain": item["domain"],
                "authors": item.get("authors", "Institutional Contributor"),
                "reliability_score": item.get("reliability_score", 0.90)
            })

        return {
            "agent": "SourceAgent (Zetaris Data Fabric)",
            "claim": claim,
            "status": "completed",
            "sources_count": len(aggregated_notes),
            "sources": sources,
            "aggregated_notes": aggregated_notes,
            "fabric_metadata": {
                "active_catalog": self.zetaris.virtual_catalog,
                "queried_pools": list(set(n["data_pool"] for n in aggregated_notes))
            }
        }
