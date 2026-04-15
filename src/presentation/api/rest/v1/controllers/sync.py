from fastapi import APIRouter
from src.infrastructure import di as dep


router = APIRouter(prefix="/api/sync", tags=["Ручная синхронизация"])


@router.post("/trigger")
async def sync_trigger(usecase: dep.AddUseCaseDep) -> dict:
    await usecase.execute()
    return {"success": True}
