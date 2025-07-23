from logging import getLogger

import jwt
from jwt import PyJWKClient


class KeycloakJWT:
    def __init__(self, jwks_uri: str):
        self.logger = getLogger(__name__)
        self.logger.info("Initializing Keycloak JWT")

        self.jwks_uri = jwks_uri
        self.jwks_client = PyJWKClient(self.jwks_uri)

    def validate_token(self, token: str) -> dict | None:
        kid = self.jwks_client.get_signing_key_from_jwt(token)
        if not kid:
            return None

        return jwt.decode(
            token, key=kid.key, algorithms=["RS256"], audience="account", verify=True
        )