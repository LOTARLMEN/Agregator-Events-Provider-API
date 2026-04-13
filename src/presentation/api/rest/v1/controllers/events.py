from fastapi import APIRouter

from src.infrastructure import di as dep


router = APIRouter(prefix="/api/events")


@router.get("")
async def get_events(usecase: dep.GetUseCaseDep):
    return await usecase.get_events()
