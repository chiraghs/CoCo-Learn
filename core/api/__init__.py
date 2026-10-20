"""core/api package - Modular FastAPI Routers for SupplyChainIQ & Digital Twin Studio."""

from core.api.routes_telemetry import router as telemetry_router
from core.api.routes_simulation import router as simulation_router
from core.api.routes_decisions import router as decisions_router
from core.api.routes_copilot import router as copilot_router
from core.api.routes_factories import router as factories_router

__all__ = [
    "telemetry_router",
    "simulation_router",
    "decisions_router",
    "copilot_router",
    "factories_router",
]
