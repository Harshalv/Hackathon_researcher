from typing import List, Dict, Any

FEDERATED_CATALOG: List[Dict[str, Any]] = [
    # AI & Computing
    {
        "id": "zetaris-ai-001",
        "pool": "zetaris.datalake.arxiv_ai_federation",
        "title": "Quantum Error Correction Thresholds and Fault-Tolerant Factoring Constraints",
        "url": "https://arxiv.org/abs/2402.11890",
        "domain": "arxiv.org",
        "authors": "Dr. Sarah Lin, Prof. Marcus Vance",
        "published_date": "2024-11-14",
        "reliability_score": 0.97,
        "keywords": ["quantum", "rsa", "encryption", "shor", "factoring", "cryptography", "qubits"],
        "summary": "Exhaustive evaluation of physical qubit architectures. Proves that factoring commercial 2048-bit RSA keys is infeasible with noisy intermediate-scale quantum (NISQ) systems and requires tens of millions of physical qubits with error rates below 10^-3.",
        "notes": "Current largest physical quantum systems (under 1,500 qubits) cannot compromise modern RSA or ECC public key cryptography. Claims of current RSA breaking by quantum computers are categorically false."
    },
    {
        "id": "zetaris-ai-002",
        "pool": "zetaris.datalake.ieee_federated_cloud",
        "title": "Artificial General Intelligence (AGI) Benchmarks and Autonomous Reasoning Frontiers",
        "url": "https://spectrum.ieee.org/ai-agi-benchmarks-2025",
        "domain": "spectrum.ieee.org",
        "authors": "Elena Rostova, IEEE AI Council",
        "published_date": "2025-01-18",
        "reliability_score": 0.94,
        "keywords": ["agi", "artificial general intelligence", "reasoning", "llm", "frontier models", "autonomous"],
        "summary": "Frontier large language models exhibit advanced contextual heuristics, programming synthesis, and mathematical theorem assistance, but lack open-ended self-directed metacognition, unified world models, and embodiment.",
        "notes": "While multimodal reasoning has achieved human-expert benchmarks in standardized examinations, consensus across AI research councils establishes that fully autonomous AGI has not yet been achieved."
    },
    {
        "id": "zetaris-ai-003",
        "pool": "zetaris.datalake.mit_tech_review",
        "title": "Transformer Attention Complexity and Linear Time State-Space Models",
        "url": "https://technologyreview.com/2024/state-space-transformers-efficiency",
        "domain": "technologyreview.com",
        "authors": "Karthik Subramanian, MIT CSAIL",
        "published_date": "2024-09-05",
        "reliability_score": 0.92,
        "keywords": ["transformer", "quadratic", "linear", "mamba", "attention", "context window", "gpu"],
        "summary": "Standard softmax self-attention scales quadratically O(N^2) with sequence length. Hybrid architectures integrating State Space Models (SSMs) and linear attention mechanisms achieve O(N) inference throughput with comparable perplexity.",
        "notes": "Quadratic compute scaling during generation remains a primary engineering bottleneck for million-token context windows in standard vanilla transformer architectures."
    },

    # Climate & Energy
    {
        "id": "zetaris-climate-001",
        "pool": "zetaris.datalake.noaa_copernicus_federation",
        "title": "Global Ocean Heat Content and Stratification Anomalies 1958-2025",
        "url": "https://www.ncei.noaa.gov/reports/ocean-heat-2025",
        "domain": "ncei.noaa.gov",
        "authors": "L. Cheng, K. Trenberth, J. Abraham",
        "published_date": "2025-01-11",
        "reliability_score": 0.99,
        "keywords": ["ocean", "heat", "climate", "warming", "temperature", "argo", "record"],
        "summary": "Comprehensive analysis of 0-2000 meter ocean heat content utilizing more than 3,800 autonomous robotic Argo profiling floats. Global ocean heat content reached unprecedented highs in 2023, 2024, and early 2025.",
        "notes": "More than 90% of excess anthropogenic heat accumulated in the Earth system is absorbed by the oceans. Unprecedented thermal expansion and marine heatwaves are empirically documented."
    },
    {
        "id": "zetaris-climate-002",
        "pool": "zetaris.datalake.iea_energy_virtual",
        "title": "Global Clean Energy Investment Trends and Levelized Cost of Electricity",
        "url": "https://www.iea.org/reports/world-energy-investment-2024",
        "domain": "iea.org",
        "authors": "International Energy Agency (IEA)",
        "published_date": "2024-06-20",
        "reliability_score": 0.96,
        "keywords": ["solar", "wind", "renewables", "lcoe", "clean energy", "cost", "fossil fuels"],
        "summary": "Utility-scale solar photovoltaic (PV) generation is currently the lowest-cost source of new electricity generation in history across most geographies, outcompeting new coal and gas power plants on a levelized cost basis.",
        "notes": "Even with grid storage balancing requirements, unsubsidized utility-scale solar PV ranges from $24 to $45/MWh in high-solar insolation regions, significantly below fossil fuel thermal generation."
    },
    {
        "id": "zetaris-climate-003",
        "pool": "zetaris.datalake.ipcc_synthesis_feed",
        "title": "Direct Air Capture and Carbon Dioxide Removal: Thermoeconomic Limits",
        "url": "https://www.ipcc.ch/report/cdr-technological-assessment",
        "domain": "ipcc.ch",
        "authors": "IPCC Working Group III",
        "published_date": "2024-04-12",
        "reliability_score": 0.98,
        "keywords": ["dac", "carbon capture", "direct air capture", "cdr", "energy penalty", "gigatons"],
        "summary": "Direct Air Capture (DAC) with chemical sorbents is technically viable for removing atmospheric CO2, but suffers from high thermodynamic minimum energy requirements (1.5-2.5 MWh per ton of CO2) and elevated capital costs ($300-$800/ton).",
        "notes": "DAC cannot substitute for immediate primary emissions abatement. Scaling DAC to gigaton-scale by 2030 without massive dedicated renewable power buildout is physically and economically restricted."
    },

    # Medicine & Healthcare
    {
        "id": "zetaris-health-001",
        "pool": "zetaris.datalake.nih_pubmed_central",
        "title": "GLP-1 Receptor Agonists and Cardiovascular Outcomes in Metabolic Syndrome",
        "url": "https://www.nejm.org/doi/full/10.1056/NEJMoa2307563",
        "domain": "nejm.org",
        "authors": "Dr. Michael Lincoff, Dr. Steven Nissen",
        "published_date": "2024-03-15",
        "reliability_score": 0.99,
        "keywords": ["glp-1", "semaglutide", "tirzepatide", "obesity", "cardiovascular", "mace", "weight loss"],
        "summary": "Large-scale randomized double-blind clinical trials (SELECT, STEP) demonstrate that GLP-1 receptor agonists reduce major adverse cardiovascular events (MACE: stroke, myocardial infarction, cardiovascular death) by approximately 20% in overweight or obese patients without diabetes.",
        "notes": "In addition to average 15-22% total body weight reduction, GLP-1 therapies provide statistically significant systemic cardioprotective and nephroprotective benefits."
    },
    {
        "id": "zetaris-health-002",
        "pool": "zetaris.datalake.who_genomics_index",
        "title": "Safety and Pharmacokinetics of Nucleoside-Modified mRNA Formulations",
        "url": "https://www.nature.com/articles/s41586-023-06103-y",
        "domain": "nature.com",
        "authors": "Weissman, D., Kariko, K., & Pardi, N.",
        "published_date": "2023-11-02",
        "reliability_score": 0.99,
        "keywords": ["mrna", "vaccine", "dna", "modification", "ribosome", "translation", "cytoplasm"],
        "summary": "In vivo biodistribution and degradation profiling shows that lipid nanoparticle-encapsulated mRNA strictly translates in the cytoplasm and is catabolized within 72 hours by endogenous cellular nucleases.",
        "notes": "mRNA lacks nuclear localization sequences and reverse-transcriptase enzymatic capability; genomic DNA alteration does not occur."
    },
    {
        "id": "zetaris-health-003",
        "pool": "zetaris.datalake.cochrane_evidence_db",
        "title": "Efficacy of Vitamin C Supplementation for Preventing Acute Respiratory Infections",
        "url": "https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD000980.pub4/full",
        "domain": "cochranelibrary.com",
        "authors": "Hemilä H, Chalker E.",
        "published_date": "2023-05-18",
        "reliability_score": 0.95,
        "keywords": ["vitamin c", "common cold", "respiratory", "prevention", "immunity", "ascorbic acid"],
        "summary": "Meta-analysis of 29 placebo-controlled trials involving 11,306 participants found that routine mega-dose vitamin C supplementation (1g/day or higher) does not reduce the incidence of the common cold in the general population.",
        "notes": "It slightly reduces cold duration (by ~8% in adults, ~14% in children) once infected, but popular assertions that high-dose Vitamin C prevents catching colds are scientifically unsupported in typical community populations."
    },

    # Economics & Finance
    {
        "id": "zetaris-econ-001",
        "pool": "zetaris.datalake.bis_central_bank_mesh",
        "title": "Central Bank Balance Sheet Quantitative Tightening and Money Supply Dynamics",
        "url": "https://www.bis.org/publ/qtrpdf/r_qt2024.htm",
        "domain": "bis.org",
        "authors": "Bank for International Settlements (BIS)",
        "published_date": "2024-07-08",
        "reliability_score": 0.96,
        "keywords": ["inflation", "interest rates", "central bank", "m2", "quantitative tightening", "liquidity"],
        "summary": "Empirical tracking of global central bank balance sheet runoff indicates significant contraction in broad M2 money supply, contributing to disinflationary trends while preserving interbank liquidity buffers.",
        "notes": "Aggressive monetary tightening cycles initiated in 2022-2023 produced the fastest global interest rate normalization in four decades, successfully cooling headline inflation toward 2-3% targets without immediate systemic banking collapse."
    },
    {
        "id": "zetaris-econ-002",
        "pool": "zetaris.datalake.reuters_market_feed",
        "title": "Semiconductor Supply Chain Geopolitics and Advanced Node Lithography",
        "url": "https://www.reuters.com/technology/semiconductor-foundry-capacity-2025-01-10/",
        "domain": "reuters.com",
        "authors": "Chun-Wei Lin, Semiconductor Intelligence Group",
        "published_date": "2025-01-10",
        "reliability_score": 0.93,
        "keywords": ["semiconductor", "tsmc", "asml", "euv", "chips", "fab", "gpu"],
        "summary": "Advanced semiconductor manufacturing under 3nm remains heavily concentrated in Taiwan (TSMC) with exclusive dependence on Dutch High-NA EUV lithography systems from ASML.",
        "notes": "Diversification initiatives across the US and Europe (CHIPS Act facilities) will increase geographical redundancy, but leading-edge node parity will take several years to reach high-yield commercial volumes."
    }
]
