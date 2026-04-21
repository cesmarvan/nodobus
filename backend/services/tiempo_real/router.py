from fastapi import APIRouter


router = APIRouter(prefix="/tiempo-real", tags=["tiempo-real"])


@router.get("/")
async def read_tiempo_real() -> dict[str, str]:
    return {
        "service": "tiempo-real",
        "message": "Tiempo real service ready",
    }


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"service": "tiempo-real", "status": "ok"}