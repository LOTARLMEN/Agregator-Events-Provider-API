__all__ = (
    "sync_router",
    "sentry_check_router",
    "events_router",
    "health_router",
    "ticket_router",
    "metrics_router",
)


from .v1.controllers.events import router as events_router
from .v1.controllers.health_check import router as health_router
from .v1.controllers.metrics import router as metrics_router
from .v1.controllers.sentry_check import router as sentry_check_router
from .v1.controllers.sync import router as sync_router
from .v1.controllers.ticket import router as ticket_router
