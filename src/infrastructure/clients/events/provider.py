import uuid
from urllib.parse import urljoin

import httpx
from async_lru import alru_cache
from httpx import ConnectTimeout, HTTPStatusError

from src.application.exceptions import ProviderError, ProviderTimeout
from src.config.config import setting
from src.infrastructure.metrics import (
    cache_hits_total,
    cache_misses_total,
    events_provider_request_duration_seconds,
    events_provider_requests_total,
)


class EventProviderClient:
    def __init__(self):
        self.base_url = setting.EVENTS_PROVIDER_BASE_URL
        self.api_key = setting.X_API_KEY

        self.headers = {"x-api-key": self.api_key}

    async def events(
        self,
        cursor: str = None,
        changed_at: str = "2000-01-01",
    ) -> dict:
        with events_provider_request_duration_seconds.labels(endpoint="/events").time():
            if cursor:
                url = cursor
                params = None
            else:
                url = urljoin(self.base_url, "events/")
                params = {"changed_at": changed_at}

            async with httpx.AsyncClient(follow_redirects=True) as client:
                try:
                    response = await client.get(
                        url, headers=self.headers, params=params
                    )
                    events_provider_requests_total.labels(
                        endpoint="/events",
                        status=response.status_code,
                    ).inc()
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
        with events_provider_request_duration_seconds.labels(
            endpoint="/register"
        ).time():
            path = f"api/events/{event_id}/register/"
            url = urljoin(self.base_url, path)
            async with httpx.AsyncClient(follow_redirects=True) as client:
                try:
                    response = await client.post(
                        url, headers=self.headers, data=user_body
                    )
                    events_provider_requests_total.labels(
                        endpoint="/register",
                        status=response.status_code,
                    ).inc()
                    response.raise_for_status()
                    return response.json()
                except ConnectTimeout:
                    raise ProviderTimeout("Provider server timed out.")
                except HTTPStatusError as e:
                    raise ProviderError(f"Provider failed to register. Error: {e}")

    async def unregister(self, event_id: uuid.UUID, ticket_id: uuid.UUID):
        with events_provider_request_duration_seconds.labels(
            endpoint="/unregister"
        ).time():
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
                    events_provider_requests_total.labels(
                        endpoint="/unregister", status=response.status_code
                    ).inc()
                    response.raise_for_status()
                except ConnectTimeout:
                    raise ProviderTimeout("Provider server timed out.")
                except HTTPStatusError as e:
                    raise ProviderError(f"Provider failed to unregister. Error: {e}")

    @alru_cache(maxsize=100, ttl=30)
    async def _cached_seats(self, event_id: uuid.UUID) -> dict[str, list[str]]:
        path = f"api/events/{event_id}/seats/"
        url = urljoin(self.base_url, path)

        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                with events_provider_request_duration_seconds.labels(
                    endpoint="/seats"
                ).time():
                    response = await client.get(url, headers=self.headers)

                events_provider_requests_total.labels(
                    endpoint="/seats", status=response.status_code
                ).inc()
                response.raise_for_status()
                return response.json()

            except ConnectTimeout:
                raise ProviderTimeout("Provider server timed out.")
            except HTTPStatusError as e:
                raise ProviderError(f"Provider failed to seats. Error: {e}")

    async def seats(self, event_id: uuid.UUID) -> dict[str, list[str]]:
        info_before = self._cached_seats.cache_info()

        result = await self._cached_seats(event_id)

        info_after = self._cached_seats.cache_info()

        if info_after.hits > info_before.hits:
            cache_hits_total.inc()
        elif info_after.misses > info_before.misses:
            cache_misses_total.inc()

        return result
