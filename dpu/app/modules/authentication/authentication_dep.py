class AuthenticationManager:
    """
    Class to be used as dependency, required for all endpoints.

    Request can originate from either
    1) A service itself fetching data -> Authenticated with hub-client
    2) A user on the website -> Authenticated normally AND ENFORCED AS STAFF USER
    """
    async def __call__(self):
        ...
