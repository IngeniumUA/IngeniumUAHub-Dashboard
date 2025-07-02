from httpx import Response

from app.modules.hub.hub_client import HubClient


class LinkClient(HubClient):
    def health_check(self) -> Response:
        client = self.client
        response: Response = client.get("")
        return response
