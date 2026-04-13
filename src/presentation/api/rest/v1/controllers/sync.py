from fastapi import APIRouter
from src.infrastructure import di as dep


router = APIRouter(prefix="/api/sync")


@router.post("/trigger")
async def sync_trigger(usecae: dep.AddUseCaseDep) -> dict:
    await usecae.execute()
    return {"success": True}
