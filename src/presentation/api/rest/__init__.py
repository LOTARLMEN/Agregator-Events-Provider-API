__all__ = (
    "sync_router",
    "events_router",
)


from .v1.controllers.sync import router as sync_router
from .v1.controllers.events import router as events_router
