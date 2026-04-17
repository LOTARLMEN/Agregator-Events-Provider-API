import uuid
from async_lru import alru_cache
import httpx
from httpx import ConnectTimeout, HTTPStatusError
from urllib.parse import urljoin
from src.application.exceptions import ProviderTimeout, ProviderError
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
            params = None
        else:
            url = urljoin(self.base_url, "events/")
            params = {"changed_at": changed_at}

        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                response = await client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                return response.json()
            except ConnectTimeout:
                raise ProviderTimeout("Provider server timed out.")
            except HTTPStatusError as e:
                raise ProviderError(f"Provider failed to register. Error: {e}")

    async def register(
        self,
        event_id: uuid.UUID,
        user_body: dict,
    ) -> dict[str, bool]:
        path = f"api/events/{event_id}/register/"
        url = urljoin(self.base_url, path)
        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                response = await client.post(url, headers=self.headers, data=user_body)
                response.raise_for_status()
                return response.json()
            except ConnectTimeout:
                raise ProviderTimeout("Provider server timed out.")
            except HTTPStatusError as e:
                raise ProviderError(f"Provider failed to register. Error: {e}")

    async def unregister(self, event_id: uuid.UUID, ticket_id: uuid.UUID):
        path = f"api/events/{event_id}/unregister/"
        url = urljoin(self.base_url, path)
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    "DELETE",
                    url,
                    json={"ticket_id": str(ticket_id)},
                    headers=self.headers,
                )
                response.raise_for_status()
            except ConnectTimeout:
                raise ProviderTimeout("Provider server timed out.")
            except HTTPStatusError as e:
                raise ProviderError(f"Provider failed to unregister. Error: {e}")

    @alru_cache(maxsize=100, ttl=30)
    async def seats(self, event_id: uuid.UUID) -> dict[str, list[str]]:
        path = f"api/events/{event_id}/seats/"
        url = urljoin(self.base_url, path)

        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()

            except ConnectTimeout:
                raise ProviderTimeout("Provider server timed out.")
            except HTTPStatusError as e:
                raise ProviderError(f"Provider failed to seats. Error: {e}")
