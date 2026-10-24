import os
from pydantic import BaseModel

class Config(BaseModel):
    # App Settings
    APP_TITLE: str = "Researcher Assistant"
    APP_VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Zetaris Settings
    ZETARIS_API_URL: str = os.getenv("ZETARIS_API_URL", "http://localhost:8080/api/v1")
    ZETARIS_API_KEY: str = os.getenv("ZETARIS_API_KEY", "")
    ZETARIS_VIRTUAL_CATALOG: str = os.getenv("ZETARIS_VIRTUAL_CATALOG", "federated_enterprise_lakehouse")
    USE_ZETARIS_SIMULATION_FALLBACK: bool = True
    
    # Meterless H-MEM Settings
    HMEM_STORAGE_DIR: str = os.getenv("HMEM_STORAGE_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "hmem"))
    HMEM_AUTO_CONSOLIDATE: bool = True
    
    # LLM Settings (optional API keys, fallback to smart deterministic reasoning engine if no external API key)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DEFAULT_LLM_PROVIDER: str = os.getenv("DEFAULT_LLM_PROVIDER", "hybrid_engine")

config = Config()
