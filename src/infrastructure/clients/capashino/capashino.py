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
            print(__name__, payload)
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method="POST",
                    url=url,
                    json=payload,
                )
                print(response.status_code)
            return response.json()
        except Exception as e:
            print(e)
            print("Ошибка при обработке Капашино.")
            print(response.status_code or 0)
