from typing import Any
import httpx
from src.config.config import setting
from urllib.parse import urljoin


class CapashinoClient:
    def __init__(self) -> None:
        self.__base_url = setting.CAPASHINO_BASE_URL
        self.__api_key = setting.X_API_KEY

        self.__headers = {"x-api-key": self.__api_key}

    async def notifications(
        self,
        payload: dict[str, Any],
    ) -> dict:
        path = "api/notifications"
        url = urljoin(self.__base_url, path)
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method="POST",
                headers=self.__headers,
                url=url,
                json=payload,
            )
            data = response.json()
            if not response.is_success:
                return None
            return data
