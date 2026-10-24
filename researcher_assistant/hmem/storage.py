import os
import json
import hashlib
from typing import List, Optional, Dict, Any
from researcher_assistant.hmem.models import MemoryNode, MemoryTier, Provenance

class HMemStorage:
    def __init__(self, storage_dir: str):
        self.storage_dir = storage_dir
        self.tiers_dir = {
            MemoryTier.L0_EPHEMERAL: os.path.join(storage_dir, "L0_ephemeral"),
            MemoryTier.L1_WORKING: os.path.join(storage_dir, "L1_working"),
            MemoryTier.L2_LONGTERM: os.path.join(storage_dir, "L2_longterm_decisions"),
        }
        self.ledger_file = os.path.join(storage_dir, "audit_ledger.jsonl")
        self._ensure_directories()
        self._seed_default_memories_if_empty()

    def _ensure_directories(self):
        os.makedirs(self.storage_dir, exist_ok=True)
        for path in self.tiers_dir.values():
            os.makedirs(path, exist_ok=True)

    def _compute_audit_hash(self, node: MemoryNode) -> str:
        payload = f"{node.compound_id}:{node.claim}:{node.decision}:{node.lineage.created_at}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

    def save_node(self, node: MemoryNode) -> MemoryNode:
        if not node.lineage.audit_hash:
            node.lineage.audit_hash = self._compute_audit_hash(node)

        tier_dir = self.tiers_dir[node.tier]
        filename = f"{node.compound_id.replace(':', '_')}.json"
        filepath = os.path.join(tier_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(node.model_dump(), f, indent=2, ensure_ascii=False)

        # Append to immutable audit ledger if it's an L2 decision
        if node.tier == MemoryTier.L2_LONGTERM:
            with open(self.ledger_file, "a", encoding="utf-8") as f:
                entry = {
                    "action": "RECORD_DECISION",
                    "compound_id": node.compound_id,
                    "claim": node.claim,
                    "decision": node.decision,
                    "confidence": node.confidence,
                    "audit_hash": node.lineage.audit_hash,
                    "timestamp": node.lineage.created_iso,
                    "supersedes": node.supersedes_id
                }
                f.write(json.dumps(entry) + "\n")

        return node

    def get_node(self, compound_id: str) -> Optional[MemoryNode]:
        for tier_dir in self.tiers_dir.values():
            filename = f"{compound_id.replace(':', '_')}.json"
            filepath = os.path.join(tier_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return MemoryNode(**data)
        return None

    def list_nodes(self, tier: Optional[MemoryTier] = None, include_archived: bool = True) -> List[MemoryNode]:
        nodes = []
        target_tiers = [tier] if tier else list(self.tiers_dir.keys())
        for t in target_tiers:
            t_dir = self.tiers_dir[t]
            if not os.path.exists(t_dir):
                continue
            for fname in sorted(os.listdir(t_dir), reverse=True):
                if fname.endswith(".json"):
                    filepath = os.path.join(t_dir, fname)
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            node = MemoryNode(**data)
                            if not include_archived and node.is_archived:
                                continue
                            nodes.append(node)
                    except Exception:
                        pass
        return nodes

    def get_ledger_entries(self) -> List[Dict[str, Any]]:
        entries = []
        if os.path.exists(self.ledger_file):
            with open(self.ledger_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            entries.append(json.loads(line))
                        except Exception:
                            pass
        return entries

    def _seed_default_memories_if_empty(self):
        """Seed rich initial historical decisions to demonstrate Meterless H-MEM decision lineage."""
        l2_nodes = self.list_nodes(MemoryTier.L2_LONGTERM)
        if len(l2_nodes) > 0:
            return

        seeds = [
            {
                "compound_id": "DEC.L2.2026.001",
                "tier": MemoryTier.L2_LONGTERM,
                "claim": "Quantum computers have broken RSA-2048 encryption in practical commercial environments",
                "summary": "Quantum supremacy claims regarding RSA-2048 cracking were examined against quantum algorithmic papers and current physical qubit counts.",
                "decision": "REFUTED",
                "confidence": 0.96,
                "explanation": "State-of-the-art quantum processors (e.g. IBM Heron, Google Willow) have ~100 to 1,000 physical qubits. Factoring RSA-2048 with Shor's algorithm requires approximately 20 million noisy physical qubits or ~4,000 logical error-corrected qubits. No commercial RSA encryption has been cracked.",
                "tags": ["cryptography", "quantum-computing", "cybersecurity"],
                "contributing_sources": [
                    {
                        "source_id": "zetaris-src-quant-01",
                        "title": "Quantum Error Correction and Resource Estimates for RSA-2048",
                        "url": "https://arxiv.org/abs/1905.09749",
                        "domain": "arxiv.org",
                        "published_date": "2024-08-15",
                        "author": "Gidney, C. & Ekerå, M.",
                        "reliability_score": 0.98,
                        "stance": "REFUTES",
                        "key_excerpt": "Factoring 2048-bit RSA keys requires 20 million noisy physical qubits under surface-code assumptions; currently available machines remain several orders of magnitude below this threshold.",
                        "relevance_score": 0.95
                    }
                ]
            },
            {
                "compound_id": "DEC.L2.2026.002",
                "tier": MemoryTier.L2_LONGTERM,
                "claim": "mRNA COVID-19 vaccines alter human nuclear DNA permanently",
                "summary": "Investigated biological mechanism of mRNA translation vs retrotranscriptase genomic integration.",
                "decision": "REFUTED",
                "confidence": 0.99,
                "explanation": "mRNA vaccines function in the cellular cytoplasm and do not enter the nucleus. mRNA molecules degrade within days after protein synthesis and lack reverse transcriptase necessary to integrate into genomic DNA.",
                "tags": ["biomedicine", "genomics", "vaccines"],
                "contributing_sources": [
                    {
                        "source_id": "zetaris-src-nih-02",
                        "title": "Molecular Biology and Cytoplasmic Fate of Synthetic mRNA Vaccines",
                        "url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8305001/",
                        "domain": "ncbi.nlm.nih.gov",
                        "published_date": "2023-01-20",
                        "author": "NIH / Nature Immunology Review",
                        "reliability_score": 0.99,
                        "stance": "REFUTES",
                        "key_excerpt": "Messenger RNA is structurally unstable and degraded via normal cellular ribonucleases within 48-72 hours. It never penetrates the nuclear membrane.",
                        "relevance_score": 0.98
                    }
                ]
            },
            {
                "compound_id": "DEC.L2.2026.003",
                "tier": MemoryTier.L2_LONGTERM,
                "claim": "Global average ocean heat content reached historic record highs in 2024-2025",
                "summary": "Analyzed Argo float measurements and NOAA Global Ocean Heat Content 0-2000m datasets federated across oceanographic datalakes.",
                "decision": "VALID",
                "confidence": 0.97,
                "explanation": "Continuous measurements from the global Argo robotic array and NOAA/Copernicus satellite altimetry confirm consecutive all-time record heat content in the upper 2000 meters of the global oceans.",
                "tags": ["climate-science", "oceanography", "geophysics"],
                "contributing_sources": [
                    {
                        "source_id": "zetaris-src-noaa-03",
                        "title": "Record-Setting Ocean Heat Content: 2024-2025 Argo Global Analysis",
                        "url": "https://www.ncei.noaa.gov/access/global-ocean-heat-content/",
                        "domain": "noaa.gov",
                        "published_date": "2025-02-10",
                        "author": "Cheng et al., NOAA NCEI & IAP/CAS",
                        "reliability_score": 0.99,
                        "stance": "SUPPORTS",
                        "key_excerpt": "The 0-2000m ocean heat content in 2024 exceeded the 2023 value by 15 zettajoules, marking the highest value ever recorded since instrumented monitoring began in 1958.",
                        "relevance_score": 0.99
                    }
                ]
            }
        ]

        for s in seeds:
            node = MemoryNode(**s)
            self.save_node(node)
