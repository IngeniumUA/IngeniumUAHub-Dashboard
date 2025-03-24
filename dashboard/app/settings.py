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


def set_db_url(environment: EnvironmentEnum) -> str:
    env_url: str | None = os.getenv("DATABASE_URL")
    if env_url is not None:
        return env_url

    # If environment is testing local testing, return test url
    if environment.value == environment.testing.value:
        return (
            "postgresql+asyncpg://postgres:password@localhost:5432/ingeniumuahub_test"
        )

    # By default assume runtime in local python interpreter, connect via localhost to dev db
    return "postgresql+asyncpg://dev-user:password@localhost:5432/dev_db"


class Settings(BaseModel):
    running_environment: EnvironmentEnum
    commit_sha: str | None

    database_url: str
    echo_sql: bool = True  # Print sql to terminal

    # Core API url
    core_api_url: str

    # Public auth uri
    keycloak_client_id: str

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
            database_url=set_db_url(environment),
            core_api_url=os.environ.get("CORE_API_URL"),
            echo_sql=True
            if environment.value
            in [EnvironmentEnum.local.value, EnvironmentEnum.testing.value]
            else False,
            keycloak_client_id=os.getenv("KEYCLOAK_CLIENT_ID", ""),
            keycloak_server_url=os.getenv("KEYCLOAK_SERVER_URL", ""),
            keycloak_realm=os.getenv("KEYCLOAK_REALM", ""),
            commit_sha=os.getenv("COMMIT_SHA", None),
        )


settings = Settings.deduce_settings()  # type: ignore
