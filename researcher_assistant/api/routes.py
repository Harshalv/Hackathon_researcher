import json
import asyncio
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from researcher_assistant.config import config
from researcher_assistant.hmem.engine import MeterlessHMemEngine
from researcher_assistant.zetaris.connector import ZetarisConnector
from researcher_assistant.agents.coordinator import ResearcherAssistantCoordinator

router = APIRouter()

# Instantiate Singletons
hmem_engine = MeterlessHMemEngine(config.HMEM_STORAGE_DIR)
zetaris_conn = ZetarisConnector(
    api_url=config.ZETARIS_API_URL,
    api_key=config.ZETARIS_API_KEY,
    virtual_catalog=config.ZETARIS_VIRTUAL_CATALOG
)
coordinator = ResearcherAssistantCoordinator(hmem_engine=hmem_engine, zetaris_connector=zetaris_conn)

class ClaimRequest(BaseModel):
    claim: str = Field(..., min_length=3, description="The proposition or claim to be investigated and evaluated.")

@router.post("/api/evaluate")
async def evaluate_claim(req: ClaimRequest):
    """Synchronous evaluation endpoint."""
    claim = req.claim.strip()
    if not claim:
        raise HTTPException(status_code=400, detail="Claim cannot be empty.")
    
    result = coordinator.evaluate_claim_sync(claim)
    return result

@router.get("/api/evaluate/stream")
async def evaluate_claim_stream(claim: str = Query(..., min_length=3)):
    """Server-Sent Events (SSE) streaming endpoint for real-time agent workflow tracking."""
    async def event_generator():
        for event in coordinator.evaluate_claim_stream(claim):
            # Short yield pause for smooth UI visualization
            await asyncio.sleep(0.35)
            data_str = json.dumps(event)
            yield f"data: {data_str}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.get("/api/hmem/decisions")
async def get_historical_decisions():
    """Returns all historical decisions preserved in Meterless H-MEM L2 Long-Term memory."""
    decisions = hmem_engine.get_all_decisions()
    return {
        "count": len(decisions),
        "decisions": [d.model_dump() for d in decisions]
    }

@router.get("/api/hmem/stats")
async def get_hmem_stats():
    """Returns H-MEM tiered storage stats and audit ledger entries."""
    stats = hmem_engine.get_stats()
    ledger = hmem_engine.storage.get_ledger_entries()
    return {
        "stats": stats,
        "recent_ledger": ledger[-10:] if ledger else []
    }

@router.post("/api/hmem/consolidate")
async def trigger_hmem_consolidation():
    """Triggers H-MEM background metabolic consolidation / sleep cycle."""
    report = hmem_engine.trigger_metabolic_consolidation()
    return report

@router.get("/api/zetaris/status")
async def get_zetaris_status():
    """Returns Zetaris Data Fabric connection and catalog status."""
    return zetaris_conn.check_connection()

@router.get("/api/sample-claims")
async def get_sample_claims():
    """Returns curated claims for one-click testing in the UI."""
    return [
        {
            "category": "Computing & Cryptography",
            "claim": "Quantum computers have broken RSA-2048 encryption in practical commercial environments",
            "expected": "REFUTED"
        },
        {
            "category": "Climate & Environment",
            "claim": "Global average ocean heat content reached historic record highs in 2024-2025",
            "expected": "VALID"
        },
        {
            "category": "Biomedicine & Genomics",
            "claim": "mRNA COVID-19 vaccines alter human nuclear DNA permanently",
            "expected": "REFUTED"
        },
        {
            "category": "Clean Energy",
            "claim": "Utility-scale solar photovoltaic is currently the lowest-cost source of new electricity generation in history",
            "expected": "VALID"
        },
        {
            "category": "Medicine & Healthcare",
            "claim": "GLP-1 receptor agonists reduce major adverse cardiovascular events in non-diabetic obese patients",
            "expected": "VALID"
        },
        {
            "category": "Nutritional Health",
            "claim": "High-dose Vitamin C supplementation prevents catching the common cold in normal populations",
            "expected": "REFUTED"
        }
    ]
