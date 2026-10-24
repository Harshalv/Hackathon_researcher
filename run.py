#!/usr/bin/env python3
"""
Convenience launcher for the Researcher Assistant application.
"""
import sys
import os
import uvicorn

# Ensure the project root is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from researcher_assistant.config import config

def main():
    print("=" * 70)
    print(" 🚀 STARTING RESEARCHER ASSISTANT")
    print(f" 🌐 Host: {config.HOST}:{config.PORT}")
    print(f" 🧠 Meterless H-MEM Storage: {config.HMEM_STORAGE_DIR}")
    print(f" 🔗 Zetaris Fabric URL: {config.ZETARIS_API_URL}")
    print("=" * 70)
    print(f" Open your browser at: http://localhost:{config.PORT}")
    print("=" * 70)
    
    uvicorn.run("researcher_assistant.main:app", host=config.HOST, port=config.PORT, reload=True)

if __name__ == "__main__":
    main()
