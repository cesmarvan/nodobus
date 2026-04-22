from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.config import get_settings
from core.database import engine
from services.incidencias.router import router as incidencias_router
from services.lineas.router import router as lineas_router


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup event
    async with engine.begin():
        pass  # Database pool initialized
    
    # Run migrations on startup (optional - you can comment this out if prefer manual migrations)
    # from alembic.config import Config
    # from alembic import command
    # alembic_cfg = Config("alembic.ini")
    # command.upgrade(alembic_cfg, "head")
    
    yield
    
    # Shutdown event
    await engine.dispose()


app = FastAPI(
    title=settings.app_name, 
    version=settings.app_version,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, object]:
    return {
        "message": "Nodobus API is running",
        "status": "ok",
        "services": ["incidencias", "lineas"],
    }


app.include_router(incidencias_router, prefix=settings.api_prefix)
app.include_router(lineas_router, prefix=settings.api_prefix)