import asyncio
import uuid

import httpx
from src.config.config import setting


class EventProviderClient:

    def __init__(self):
        self.base_url = setting.EVENTS_PROVIDER_BASE_URL
        self.api_key = setting.EVENTS_PROVIDER_API_KEY

        self.headers = {"x-api-key": self.api_key}

    async def events(
        self,
        cursor: str = None,
        changed_at: str = "2000-01-01",
    ) -> dict:
        if cursor:
            url = cursor
        else:
            url = f"{self.base_url}/events/?changed_at={changed_at}"

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, headers=self.headers)

            response.raise_for_status()

            return response.json()

    async def register(
        self,
        event_id: uuid.UUID,
        user_body: dict,
    ) -> dict[str, bool]:
        url = f"{self.base_url}/api/events/{event_id}/register/"

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.post(url, headers=self.headers, data=user_body)

            response.raise_for_status()

            return response.json()

    async def unregister(
        self,
        event_id: uuid.UUID,
        ticket_body: dict,
    ) -> dict[str, bool]:
        url = f"{self.base_url}/api/events/{event_id}/unregister"

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.post(url, headers=self.headers, data=ticket_body)

            response.raise_for_status()

            return response.json()

    async def seats(self, event_id: uuid.UUID) -> dict[str, list[str]]:
        url = f"{self.base_url}/api/events/{event_id}/seats"

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, headers=self.headers)

            response.raise_for_status()

            return response.json()


async def main():
    client = EventProviderClient()
    events = await client.events()
    for event in events:
        print(event)


if __name__ == "__main__":
    asyncio.run(main())
