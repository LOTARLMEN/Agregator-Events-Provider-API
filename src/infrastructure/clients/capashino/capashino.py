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
        try:
            # print(__name__, response.text)
            # print(__name__, response.request)
            # print(__name__, response.json())
            print(
                __name__,
            )
            async with httpx.AsyncClient(follow_redirects=True, timeout=5) as client:
                response = await client.post(
                    url,
                    headers=self.__headers,
                    json=payload,
                )
                print(response.status_code)
            return response.json()
        except Exception as e:
            print(__name__, e)
            print(response.status_code or 0)
