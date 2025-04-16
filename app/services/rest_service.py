import httpx

from app.config import settings


class RestService:
    def __init__(self, auth_token: str = None):
        self.base_url = settings.REST_SERVICE_BASE_URL
        self.timeout = settings.REST_SERVICE_TIMEOUT
        self.auth_token = auth_token

    async def get_data(self, endpoint: str, params: dict = None):
        headers = {}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/{endpoint}", params=params, headers=headers
            )
            response.raise_for_status()
            return response.json()

    async def post_data(self, endpoint: str, data: dict):
        headers = {}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(f"{self.base_url}/{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
