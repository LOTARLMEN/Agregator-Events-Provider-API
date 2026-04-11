import httpx
from src.config.config import setting


class EventProviderClient:

    def __init__(self):
        self.base_url = setting.DATABASE_URL
        self.api_key = setting.EVENTS_PROVIDER_API_KEY

        self.headers = {"x-api-key": self.api_key}
