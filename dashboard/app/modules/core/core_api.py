from typing import Optional

from keycloak import KeycloakOpenID

from app.settings import settings


class CoreClient:
    def __init__(self, username: str, password: str):
        self.keycloak_token: Optional[dict] = None

        self.username = username
        self.password = password

    def _keycloak_access_token(self):
        keycloak_openid = KeycloakOpenID(
            server_url=settings.keycloak_server_url,
            client_id="backend-api",
            realm_name="master",
        )
        self.keycloak_token = keycloak_openid.token(self.username, self.password)
