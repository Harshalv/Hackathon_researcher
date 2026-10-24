from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import time
import uuid

class MemoryTier(str, Enum):
    L0_EPHEMERAL = "L0_ephemeral"       # Session queries, raw inputs
    L1_WORKING = "L1_working"           # Analyser intermediate reasoning, notes clusters
    L2_LONGTERM = "L2_longterm_decision"# Immutable decisions, vetted claims, precedents

class DecisionStatus(str, Enum):
    VALID = "VALID"
    REFUTED = "REFUTED"
    PARTIALLY_VALID = "PARTIALLY_VALID"
    INCONCLUSIVE = "INCONCLUSIVE"

class StanceType(str, Enum):
    SUPPORTS = "SUPPORTS"
    REFUTES = "REFUTES"
    PARTIALLY_SUPPORTS = "PARTIALLY_SUPPORTS"
    NEUTRAL = "NEUTRAL"
    INCONCLUSIVE = "INCONCLUSIVE"

class SourceCitation(BaseModel):
    source_id: str
    title: str
    url: str
    domain: str
    published_date: Optional[str] = None
    author: Optional[str] = None
    reliability_score: float = 0.85
    stance: StanceType = StanceType.NEUTRAL
    key_excerpt: str
    relevance_score: float = 0.90

class Provenance(BaseModel):
    created_at: float = Field(default_factory=time.time)
    created_iso: str = Field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    agents_involved: List[str] = Field(default_factory=lambda: ["source", "analyser", "evaluator"])
    parent_decision_id: Optional[str] = None
    audit_hash: Optional[str] = None

class MemoryNode(BaseModel):
    compound_id: str  # e.g., L2.2026.001 or L1.claim.002
    tier: MemoryTier
    claim: str
    summary: str
    decision: Optional[DecisionStatus] = None
    confidence: float = 0.0
    explanation: Optional[str] = None
    contributing_sources: List[SourceCitation] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    lineage: Provenance = Field(default_factory=Provenance)
    is_archived: bool = False
    supersedes_id: Optional[str] = None
    superseded_by: Optional[str] = None
    historical_notes: Optional[str] = None
