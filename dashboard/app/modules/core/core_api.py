from datetime import datetime, timezone
from typing import Optional
import httpx
from httpx import Client, Response

from keycloak import KeycloakOpenID
from pydantic import TypeAdapter

from app.settings import settings


class CoreClient:  # todo rename to CoreAPI
    """
    Meant for communication between the streamlit backend server and core application.
    Note it does not use any user authentication, but an API account.
    """

    def __init__(self, connection_timeout: float = 10.0):
        self._keycloak_start: datetime | None = None
        self._keycloak_token: Optional[dict] = None
        self.connection_timeout: float = connection_timeout  # In seconds

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
        return httpx.Client(base_url=settings.core_api_url,
                            headers=headers,
                            timeout=self.connection_timeout)

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
        query_param = dict(limit=limit, offset=offset)
        response = self.client.get("/api/v1/transaction", params=query_param)
        return TypeAdapter(list[dict]).validate_json(response.content)

    def query_hubcheckouttrackers(
        self, limit: int = 100, offset: int = 50, **kwargs
    ) -> list[dict]:
        query_param = dict(limit=limit, offset=offset)
        response = self.client.get("/api/v1/checkout/tracker", params=query_param)
        return TypeAdapter(list[dict]).validate_json(response.content)

    def query_hubcheckouts(
        self, limit: int = 100, offset: int = 50, **kwargs
    ) -> list[dict]:
        query_param = dict(limit=limit, offset=offset)
        response = self.client.get("/api/v1/checkout", params=query_param)
        return TypeAdapter(list[dict]).validate_json(response.content)

    def count_transactions(self, **kwargs) -> int:
        query_param = {}
        response = self.client.get("/api/v1/transaction/count", params=query_param)
        return TypeAdapter(int).validate_json(response.content)

    def count_hubcheckouttrackers(self, **kwargs) -> int:
        query_param = {}
        response = self.client.get("/api/v1/checkout/tracker/count", params=query_param)
        return TypeAdapter(int).validate_json(response.content)

    def count_hubcheckouts(self, **kwargs) -> int:
        query_param = {}
        response = self.client.get("/api/v1/checkout/count", params=query_param)
        return TypeAdapter(int).validate_json(response.content)
