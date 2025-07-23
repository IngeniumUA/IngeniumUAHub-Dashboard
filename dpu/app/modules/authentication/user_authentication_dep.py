from logging import getLogger
from typing import Optional, Annotated

from fastapi import Depends
from jwt import exceptions as jwt_exceptions
from starlette.requests import HTTPConnection

from app.modules.authentication.keycloak_jwt import KeycloakJWT
from app.settings import settings


class HubAuthManager:
    def __init__(self, token_interface=None):
        self.logger = getLogger(__name__)
        if token_interface is None:
            token_interface = KeycloakJWT(settings.keycloak_jwks_uri)
        self.keycloak_jwt = token_interface

    async def __call__(self, conn: HTTPConnection):
        return await self.get_user(conn=conn)

    async def get_user(
        self, conn: HTTPConnection
    ) -> dict | None:
        token = self.get_bearer_token(conn)
        if not token:
            return None

        # Validate the token, if it is invalid return None
        try:
            sso_user = self.keycloak_jwt.validate_token(token)
        except Exception as exception:
            # Expired signatures will probably happen, but something else might be a problem
            if (
                exception.__class__.__name__
                != jwt_exceptions.ExpiredSignatureError.__name__
            ):
                self.logger.warning(
                    "Could not validate token with cause: %s", exception
                )
            return None

        # Check the client is user auth
        if sso_user.get("client_id") != settings.keycloak_frontend_client_id:
            return None

        # Make sure that the required fields are present in the JWT token
        if not sso_user or not self.validate_jwt_data(sso_user):
            self.logger.warning("JWT token data is missing fields!")
            return None
        return sso_user

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

    @classmethod
    def validate_jwt_data(cls, data: dict) -> bool:
        """
        Returns false if any of the required fields are missing

        @param data: SSO Token
        @return:
        """
        return all(key in data for key in ["email", "given_name", "family_name", "sub"])


auth_manager = HubAuthManager()  # Initialise for use in dependencies
UserAuthDep = Annotated[Optional[dict], Depends(auth_manager)]