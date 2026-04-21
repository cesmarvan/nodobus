from fastapi import APIRouter


router = APIRouter(prefix="/incidencias", tags=["incidencias"])


@router.get("/")
async def read_incidencias() -> dict[str, str]:
    return {
        "service": "incidencias",
        "message": "Incidencias service ready",
    }


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"service": "incidencias", "status": "ok"}