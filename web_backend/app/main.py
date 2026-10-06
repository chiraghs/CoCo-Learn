from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.routes.facilities import router as facilities_router
from app.routes.rules import router as rules_router
from app.routes.cortex import router as cortex_router

app = FastAPI(
    title="SupplyChainIQ Digital Twin & Governed Analytics API",
    description="Enterprise API backed by Snowflake CoCo, Cortex Analyst & Action MCP",
    version="2.0.0"
)

# Enable CORS for local Vite development and web hosting
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route modules
app.include_router(facilities_router)
app.include_router(rules_router)
app.include_router(cortex_router)

@app.get("/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": "SupplyChainIQ API Gateway",
        "backend": "Snowflake Account ZJXLXUZ.JV50315",
        "semantic_layer": "Active"
    }

# Serve compiled frontend static files if present
frontend_dist = os.path.join(os.path.dirname(__file__), "../../web_frontend/dist")
if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
