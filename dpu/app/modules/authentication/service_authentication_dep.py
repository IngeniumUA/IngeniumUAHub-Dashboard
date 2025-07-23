from logging import getLogger
from typing import Annotated, Optional

from fastapi import Depends
from jwt import ExpiredSignatureError
from starlette.requests import HTTPConnection

from app.modules.authentication.keycloak_jwt import KeycloakJWT
from app.settings import settings


class HubServiceAuthenticationManager:
    def __init__(self, token_interface=None):
        self.logger = getLogger(__name__)
        if token_interface is None:
            token_interface = KeycloakJWT(settings.keycloak_jwks_uri)
        self.keycloak_jwt = token_interface

    async def __call__(self, conn: HTTPConnection):
        return await self.get_service_account(conn=conn)

    async def get_service_account(self, conn: HTTPConnection):
        token = self.get_bearer_token(conn)
        if not token:
            return None

        # Validate the token, if it is invalid return None
        try:
            return self.keycloak_jwt.validate_token(token)
        except ExpiredSignatureError:
            return None
        except Exception as e:
            raise e

    @classmethod
    def get_bearer_token(cls, conn: HTTPConnection) -> str | None:
        """
        Retrieve the Bearer token from the Authorization header

        @param conn: HTTPConnection via Dependency Injection
        @return: Bearer token if parsed
        """
        # Get the token from the Authorization header
        authorization = conn.headers.get("Authorization", None)
        if not authorization:
            return None

        # Check if the token is a Bearer token
        scheme, token = authorization.split(" ")
        if scheme.lower() != "bearer":
            return None

        return token


# Initialise it once
hub_service_authentication_manager = HubServiceAuthenticationManager()

# Dependencies for use in code
HubAuthDep = Depends(hub_service_authentication_manager)
HubAuthAnnotatedDep = Annotated[Optional[dict], HubAuthDep]