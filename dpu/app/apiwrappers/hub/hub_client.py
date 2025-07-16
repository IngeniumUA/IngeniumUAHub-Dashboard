from datetime import datetime, timezone
from typing import Optional, Any
from httpx import Response, AsyncClient

from keycloak import KeycloakOpenID
from pydantic import BaseModel, ConfigDict, TypeAdapter

from app.modules.exception.hubexception import HubException
from app.settings import settings

class HubExceptionDetail(BaseModel):
    error_nl: str
    error_en: str

    # Allow other fields than the ones specified above
    model_config = ConfigDict(
        extra="allow",
    )

class HubExceptionResponse(BaseModel):
    detail: HubExceptionDetail


class HubClient:
    """
    Meant for communication between the streamlit backend server and core application.
    Note it does not use any user authentication, but an API account.
    """

    def __init__(self, base_url: str, connection_timeout: float = 10.0):
        self.base_url = base_url

        self.connection_timeout: float = connection_timeout  # In seconds

        self._keycloak_start: datetime | None = None
        self._keycloak_token: Optional[dict] = None

        self._client: Optional[AsyncClient] = None

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
    def client(self) -> AsyncClient:
        if self._client is None:
            headers = {
                "Authorization": f"Bearer {self.keycloak_token['access_token']}",
            }
            self._client = AsyncClient(base_url=self.base_url, headers=headers, timeout=self.connection_timeout)
        return self._client

    @classmethod
    def _keycloak_access_token(cls):
        keycloak_openid = KeycloakOpenID(
            server_url=settings.keycloak_server_url,
            client_id=settings.keycloak_backend_client_id,
            realm_name=settings.keycloak_realm,
            client_secret_key=settings.keycloak_client_secret,
        )
        return keycloak_openid.token(grant_type="client_credentials")

    async def health_check(self) -> Response:
        client = self.client
        response: Response = await client.get("/health")
        return response

    async def auth_check(self) -> dict:
        client = self.client
        response: Response = await client.get("/auth/check")
        return {"status_code": response.status_code, "response": response.text}

    @classmethod
    def handle_response(cls, response: Response, response_type: Any):
        print(response.content)
        if response.status_code != 200:
            response_type = HubExceptionResponse
        if response.json():
            return TypeAdapter(response_type).validate_json(response.content)
        raise HubException.not_implemented()
