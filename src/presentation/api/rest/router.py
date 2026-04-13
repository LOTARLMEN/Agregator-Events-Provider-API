from fastapi import APIRouter
from . import sync_router
from . import events_router


router = APIRouter()

router.include_router(sync_router)
router.include_router(events_router)
