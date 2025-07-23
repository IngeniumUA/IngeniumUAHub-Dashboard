from app.modules.authentication.service_authentication_dep import HubAuthAnnotatedDep
from app.modules.authentication.user_authentication_dep import UserAuthDep
from app.modules.exception.hubexception import HubException


class AuthenticationManager:
    """
    Class to be used as dependency, required for all endpoints.

    Request can originate from either
    1) A service itself fetching data -> Authenticated with hub-client
    2) A user on the website -> Authenticated normally AND ENFORCED AS STAFF USER
    """
    async def __call__(self,
                       hub_auth: HubAuthAnnotatedDep,
                       user_auth: UserAuthDep
                       ):
        if hub_auth is None and user_auth is None:
            raise HubException.must_be_authenticated()

        if hub_auth is not None and user_auth is None:
            return hub_auth

        if "staff" not in user_auth.get("realm_access", {}).get("roles", []):
            raise HubException.must_be_authenticated()
