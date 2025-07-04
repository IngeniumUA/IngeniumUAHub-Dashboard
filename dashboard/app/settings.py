import os
import sys
from logging import getLogger
from enum import IntEnum

from pydantic import BaseModel

logger = getLogger(__name__)


class EnvironmentEnum(IntEnum):
    """
    Differentiate production as 'Live' application and staging as 'pseudo-live'.
    Dev is for *local* development op application.
    Testing when running any type of automated test
    """

    production = 1
    local = 2
    testing = 3
    staging = 4


def set_environment() -> EnvironmentEnum:
    if "pytest" in sys.modules:
        return EnvironmentEnum.testing

    # If env is null or equal to production, return running
    envi: str | None = os.getenv("ENVIRONMENT")
    if envi == "production":
        return EnvironmentEnum.production
    if envi == "staging":
        return EnvironmentEnum.staging

    return EnvironmentEnum.local


class Settings(BaseModel):
    running_environment: EnvironmentEnum
    commit_sha: str | None

    echo_sql: bool = True  # Print sql to terminal

    # HUB API urls
    core_api_url: str
    dpu_api_url: str

    # Umami
    umami_username: str
    umami_password: str

    # Public auth
    keycloak_frontend_client_id: str
    keycloak_jwks_uri: str

    # Service auth
    keycloak_backend_client_id: str
    keycloak_client_secret: str

    azure_storage_key: str | None

    # Admin
    # Keycloak variables
    keycloak_server_url: str  # i.e. https://sso.ingeniumua.be
    keycloak_realm: str

    def is_debug(self) -> bool:
        return self.running_environment.name in [
            EnvironmentEnum.local.name,
            EnvironmentEnum.testing.name,
        ]

    @classmethod
    def deduce_settings(cls) -> "Settings":
        return Settings(
            running_environment=(environment := set_environment()),
            core_api_url=os.environ.get("CORE_API_URL"),
            dpu_api_url=os.environ.get("DPU_API_URL"),
            echo_sql=True
            if environment.value
            in [EnvironmentEnum.local.value, EnvironmentEnum.testing.value]
            else False,
            keycloak_jwks_uri=os.environ.get("KEYCLOAK_JWKS_URI"),
            keycloak_backend_client_id=os.getenv("KEYCLOAK_BACKEND_CLIENT_ID", ""),
            keycloak_frontend_client_id=os.getenv("KEYCLOAK_FRONTEND_CLIENT_ID", ""),
            keycloak_client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET", ""),
            keycloak_server_url=os.getenv("KEYCLOAK_SERVER_URL", ""),
            keycloak_realm=os.getenv("KEYCLOAK_REALM", ""),
            commit_sha=os.getenv("COMMIT_SHA", None),
            umami_username=os.getenv("UMAMI_USERNAME", ""),
            umami_password=os.getenv("UMAMI_PASSWORD", ""),
            azure_storage_key=os.getenv("AZURE_STORAGE_KEY", None)
        )


settings = Settings.deduce_settings()  # type: ignore
