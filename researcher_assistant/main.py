import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from researcher_assistant.config import config
from researcher_assistant.api.routes import router as api_router

app = FastAPI(
    title=config.APP_TITLE,
    version=config.APP_VERSION,
    description="Multi-agent claim verification assistant with Zetaris Data Fabric & Meterless H-MEM"
)

# Static files directory
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include API routes
app.include_router(api_router)

@app.get("/")
async def root():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Researcher Assistant API active. Static UI not found."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("researcher_assistant.main:app", host=config.HOST, port=config.PORT, reload=True)
