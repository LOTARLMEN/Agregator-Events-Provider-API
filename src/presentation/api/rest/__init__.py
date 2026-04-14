__all__ = ("sync_router", "events_router", "health_router", "ticket_router")


from .v1.controllers.sync import router as sync_router
from .v1.controllers.events import router as events_router
from .v1.controllers.health_check import router as health_router
from .v1.controllers.ticket import router as ticket_router
