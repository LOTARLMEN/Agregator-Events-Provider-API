from src.infrastructure.clients.events.provider import EventProviderClient


class EventsPaginator:
    def __init__(
        self,
        client: EventProviderClient,
        start_changed_at: str = "2000-01-01",
    ):
        self.client = client
        self.start_changed_at = start_changed_at

    async def __aiter__(self):
        next_page = None

        while True:
            result = await self.client.events(
                cursor=next_page, changed_at=self.start_changed_at
            )
            yield result["results"]

            next_page = result["next"]
            if not next_page:
                break
