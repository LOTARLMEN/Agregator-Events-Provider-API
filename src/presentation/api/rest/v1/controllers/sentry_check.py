from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Проверка SDK"])


@router.get("/debug-sentry")
async def trigger_error():
    return 1 / 0
