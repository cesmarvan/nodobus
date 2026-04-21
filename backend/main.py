from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from services.incidencias.router import router as incidencias_router
from services.tiempo_real.router import router as tiempo_real_router


app = FastAPI(title=settings.app_name, version=settings.app_version)

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
        "services": ["incidencias", "tiempo-real"],
    }


app.include_router(incidencias_router, prefix=settings.api_prefix)
app.include_router(tiempo_real_router, prefix=settings.api_prefix)