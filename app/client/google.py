from dataclasses import dataclass

import httpx

from app.schema import GoogleUserData
from settings import Settings


@dataclass
class GoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_user_access_token(code=code)
        response = await self.async_client.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        data = response.json()
        if "error" in data:
            raise ValueError(
                f"Error fetching user info: {
                data['error']} - {data.get('error_description')}"
            )
        return GoogleUserData(**data, access_token=access_token)

    async def _get_user_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_SECRET_KEY,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        }

        response = await self.async_client.post(
            self.settings.GOOGLE_TOKEN_URL,
            data=data
        )
        return response.json()["access_token"]
