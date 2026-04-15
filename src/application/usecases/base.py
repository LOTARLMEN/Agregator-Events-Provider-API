from src.infrastructure.clients.events.provider import EventProviderClient
from src.infrastructure.db.uow import UnitOfWork


class BaseUseCase:
    def __init__(self, uow: UnitOfWork, client: EventProviderClient):
        self.uow = uow
        self.client = client
