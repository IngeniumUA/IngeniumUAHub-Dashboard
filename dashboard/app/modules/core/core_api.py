from datetime import datetime, timezone
from typing import Optional
import httpx
from httpx import Client, Response

from keycloak import KeycloakOpenID

from app.settings import settings


class CoreClient:  # todo rename to CoreAPI
    """
    Meant for communication between the streamlit backend server and core application.
    Note it does not use any user authentication, but an API account.
    """

    def __init__(self):
        self._keycloak_start: datetime | None = None
        self._keycloak_token: Optional[dict] = None

    @property
    def keycloak_token(self):
        if self._keycloak_token is None:
            self._keycloak_token = self._keycloak_access_token()
            self._keycloak_start = datetime.now(timezone.utc)

        if (
            datetime.now(timezone.utc) - self._keycloak_start
        ).total_seconds() > self._keycloak_token["expires_in"]:
            # TODO Use refresh token instead of just fetching new access token
            self._keycloak_token = self._keycloak_access_token()

        return self._keycloak_token

    @property
    def client(self) -> Client:
        headers = {
            "Authorization": f"Bearer {self.keycloak_token['access_token']}",
        }
        return httpx.Client(base_url=settings.core_api_url, headers=headers)

    @classmethod
    def _keycloak_access_token(cls):
        keycloak_openid = KeycloakOpenID(
            server_url=settings.keycloak_server_url,
            client_id=settings.keycloak_client_id,
            realm_name=settings.keycloak_realm,
            client_secret_key=settings.keycloak_client_secret,
        )
        return keycloak_openid.token(grant_type="client_credentials")

    def health_check(self) -> dict:
        client = self.client
        response: Response = client.get("")
        return {"status_code": response.status_code, "response": response.text}

    def auth_check(self) -> dict:
        client = self.client
        response: Response = client.get("/auth/check")
        return {"status_code": response.status_code, "response": response.text}

    def query_transactions(
        self, limit: int = 100, offset: int = 50, **kwargs
    ) -> list[dict]:
        query_param = {}
        response = self.client.get("/api/v1/transaction", params=query_param)
        return response.text  # fixme
