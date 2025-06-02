from datetime import datetime, timezone
from typing import Optional
from httpx import Client, Response
from pydantic import BaseModel, TypeAdapter


class UmamiTokenUser(BaseModel):
    """
    Just used for parsing
    """

    id: str  # Looks like uuid
    username: str
    createdAt: datetime


class UmamiToken(BaseModel):
    token: str
    user: UmamiTokenUser


class UmamiClient:
    def __init__(
        self,
        username: str,
        password: str,
        base_url: str,
        connection_timeout: float = 10.0,
    ):
        self.username = username
        self.password = password

        self.base_url = base_url
        self.connection_timeout = connection_timeout

        self._token_start: datetime | None = None
        self._token: Optional[UmamiToken] = None

    @property
    def token(self):
        if self._token is None:
            self._token = self._request_token()
            self._token_start = datetime.now(timezone.utc)

        if (
            datetime.now(timezone.utc) - self._token_start
        ).total_seconds() > 60 * 60 * 24 * 31:  # No time on token it seems
            self._token = self._request_token()

        return self._token

    def _request_token(self) -> Optional[UmamiToken]:
        with Client(base_url=self.base_url, timeout=self.connection_timeout) as client:
            response = client.post(
                "/api/auth/login",
                json={"username": self.username, "password": self.password},
            )
            if response.status_code != 200:
                return None
            return TypeAdapter(UmamiToken).validate_json(response.json())

    @property
    def client(self) -> Client:
        headers = {
            "Authorization": f"Bearer {self.token['access_token']}",
        }
        return Client(
            base_url=self.base_url, headers=headers, timeout=self.connection_timeout
        )

    def health_check(self) -> dict:
        client = self.client
        response: Response = client.get("")
        return {"status_code": response.status_code, "response": response.text}

    def auth_check(self) -> dict:
        client = self.client
        response: Response = client.get("/api/auth/verify")
        return {"status_code": response.status_code, "response": response.text}
