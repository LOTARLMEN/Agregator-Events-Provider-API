from fastapi import APIRouter
from . import (
    sync_router,
    events_router,
    health_router,
    ticket_router,
    sentry_check_router,
)


router = APIRouter()

router.include_router(sync_router)
router.include_router(health_router)
router.include_router(events_router)
router.include_router(ticket_router)
router.include_router(sentry_check_router)
