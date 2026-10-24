# 🔬 Researcher Assistant

An autonomous multi-agent verification and claim evaluation system powered by **Zetaris Data Fabric** as a data aggregator and **Meterless H-MEM** (Hierarchical Memory) to track and remember historical decisions.

Featuring a sleek, modern UI for entering claims, tracking live multi-agent execution, viewing verdicts with confidence metrics, reading comprehensive explanations, and exploring contributing article links.

---

## 🏛️ System Architecture

```
                                  [ User Claim Input ]
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                             Researcher Assistant Core                               │
│                                                                                     │
│  ┌─────────────────────────┐                ┌────────────────────────────────────┐  │
│  │   Meterless H-MEM       │                │      Zetaris Data Fabric           │  │
│  │  Hierarchical Memory    │                │  (Distributed Query Aggregator)    │  │
│  │  - L0 Ephemeral Input   │                │  - Virtual Catalogs & Data Pools   │  │
│  │  - L1 Working Notes     │                │  - Query-in-Place Federated Mesh   │  │
│  │  - L2 Decision Ledger   │                │  - PubMed, ArXiv, NOAA, IEA, etc.  │  │
│  └───────────┬─────────────┘                └─────────────────┬──────────────────┘  │
│              │ (Past Decisions Recall)                        │ (Evidence Notes)    │
│              ▼                                                ▼                     │
│    ┌───────────────────┐    Aggregated Notes     ┌────────────────────────┐         │
│    │   Source Agent    │ ──────────────────────> │     Analyser Agent     │         │
│    │ (Zetaris Driver)  │                         │(Validates notes vs clm)│         │
│    └───────────────────┘                         └───────────┬────────────┘         │
│                                                              │ Stance & Breakdown   │
│                                                              ▼                      │
│                                                  ┌────────────────────────┐         │
│                                                  │    Evaluator Agent     │         │
│                                                  │(Verdict & Explanation) │         │
│                                                  └───────────┬────────────┘         │
│                                                              │                      │
│                                  Persist Decision Compound ID│ (e.g. DEC.L2.2026...)│
│                                                              ▼                      │
│                                                  ┌────────────────────────┐         │
│                                                  │   Meterless H-MEM L2   │         │
│                                                  │ Immutable Audit Ledger │         │
└──────────────────────────────────────────────────────────────┴──────────────────────┘
                                                               │
                                                               ▼
                                       [ Sleek Glassmorphic Web UI ]
                                       - Interactive Claim Input Bar
                                       - Live Agent Pipeline Telemetry (SSE)
                                       - Decision Badge & Confidence Meter
                                       - Contributing Articles with Links
                                       - Meterless H-MEM Memory Vault
```

---

## 🤖 The 3 Autonomous Agents

### 1. `SourceAgent` (Zetaris Data Fabric Aggregator)
- Connects to the **Zetaris Data Fabric** query engine.
- Employs a query-in-place architecture across multi-cloud and federated enterprise pools (e.g. `arxiv_ai_federation`, `nih_pubmed_central`, `noaa_copernicus_federation`, `iea_energy_virtual`, `who_genomics_index`).
- Gathers relevant source citations, observational notes, authors, publication dates, and source reliability weights without duplicate physical data copying.

### 2. `AnalyserAgent` (Claim vs. Notes Validation)
- Analyzes aggregated notes gathered by `SourceAgent` to check whether the input claim is factually valid as per the notes.
- Performs multi-vector stance detection: `SUPPORTS`, `REFUTES`, `PARTIALLY_SUPPORTS`, or `INCONCLUSIVE`.
- Evaluates evidence weights, reliability scores, and nuance/caveat detection.
- Cross-references relevant historical precedents recalled from **Meterless H-MEM** to prevent contradictions across evaluation cycles.

### 3. `EvaluatorAgent` (Decision Synthesis & Citation Mapping)
- Receives the synthesized evidence analysis from `AnalyserAgent`.
- Delivers an overall verdict: **`VALID`**, **`REFUTED`**, **`PARTIALLY_VALID`**, or **`INCONCLUSIVE`**.
- Computes a calibrated confidence score (0-100%).
- Generates an explanation detailing **why** the claim is valid or not, quoting key empirical data and caveats.
- Surfaces **Contributing Articles** with interactive links (`target="_blank"`), stance indicators, reliability ratings, and excerpts.
- Commits the new decision record into **Meterless H-MEM L2 Long-Term Memory** with an immutable compound ID (e.g. `DEC.L2.2026.004`) and cryptographic audit hash.

---

## 🧠 Meterless H-MEM Integration

The system incorporates the **Meterless H-MEM** (Hierarchical Memory) architecture to remember historical decisions:

1. **Tiered Storage Pyramid**:
   - `L0 Ephemeral`: Session queries and raw inputs.
   - `L1 Working Memory`: Intermediate notes clusters and analyser working tokens.
   - `L2 Long-Term Decisions`: Immutable historical decisions with compound IDs (e.g. `DEC.L2.2026.001`).
2. **Provenance & Trust Lineage**:
   - Every historical decision carries metadata: session ID, agents involved, source citations, audit SHA-256 hash, and precedent pointers.
3. **No Overwrite Policy**:
   - Historical decisions are never silently wiped; superseded or refined claims are cross-referenced so future agents learn why previous stances were formed or updated.
4. **Metabolic Maintenance ("Sleep/Dream" Cycles)**:
   - Built-in consolidation routine that audits decision clusters, assesses coherence, and reports memory statistics.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.9+ (or `uv` / `pip`)

### 2. Installation
```bash
# Clone or navigate to the workspace
cd c:\Harshal\projects\hackathon_researcher

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Application
```bash
python run.py
```
Or with `uvicorn`:
```bash
uvicorn researcher_assistant.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Open the Sleek UI
Navigate in your browser to:
**`http://localhost:8000`**

---

## 🧪 Test Claims Included in the UI
The UI features one-click test pills across multiple scientific and technical fields:

| Category | Claim | Expected Verdict |
| :--- | :--- | :--- |
| **Computing & Cryptography** | *"Quantum computers have broken RSA-2048 encryption in practical commercial environments"* | **`REFUTED`** |
| **Climate & Oceanography** | *"Global average ocean heat content reached historic record highs in 2024-2025"* | **`VALID`** |
| **Genomics & Vaccines** | *"mRNA COVID-19 vaccines alter human nuclear DNA permanently"* | **`REFUTED`** |
| **Clean Energy** | *"Utility-scale solar photovoltaic is currently the lowest-cost source of new electricity generation in history"* | **`VALID`** |
| **Pharmacology** | *"GLP-1 receptor agonists reduce major adverse cardiovascular events in non-diabetic obese patients"* | **`VALID`** |
| **Nutritional Health** | *"High-dose Vitamin C supplementation prevents catching the common cold in normal populations"* | **`REFUTED`** |

---

## 📡 API Endpoints

- `POST /api/evaluate`: Submit a claim JSON `{ "claim": "..." }` for full evaluation.
- `GET /api/evaluate/stream?claim=...`: SSE endpoint streaming live multi-agent pipeline steps.
- `GET /api/hmem/decisions`: Retrieve all recorded historical decisions from H-MEM L2 storage.
- `GET /api/hmem/stats`: Return memory tier counts and audit ledger records.
- `POST /api/hmem/consolidate`: Trigger H-MEM metabolic consolidation (sleep/dream cycle).
- `GET /api/zetaris/status`: Check Zetaris fabric and federated catalog status.
- `GET /api/sample-claims`: Retrieve pre-configured sample claims.
