from pydantic import TypeAdapter

from app.modules.hub.hub_client import HubClient

class CoreClient(HubClient):
    def internal_summarised(self):
        response = self.client.get("/api/v1/internal/summarised")
        return TypeAdapter(dict[str, int]).validate_json(response.content)

    def query_transactions(
        self, limit: int = 100, offset: int = 0, **kwargs
    ) -> list[dict]:
        query_param = dict(limit=limit, offset=offset)
        response = self.client.get("/api/v1/transaction", params=query_param)
        return TypeAdapter(list[dict]).validate_json(response.content)

    def query_hubcheckouttrackers(
        self, limit: int = 100, offset: int = 0, **kwargs
    ) -> list[dict]:
        query_param = dict(limit=limit, offset=offset)
        response = self.client.get("/api/v1/checkout/tracker", params=query_param)
        return TypeAdapter(list[dict]).validate_json(response.content)

    def query_hubcheckouts(
        self, limit: int = 100, offset: int = 0, **kwargs
    ) -> list[dict]:
        query_param = dict(limit=limit, offset=offset)
        response = self.client.get("/api/v1/checkout", params=query_param)
        return TypeAdapter(list[dict]).validate_json(response.content)

    def count_transactions(self, **kwargs) -> int:
        query_param = {}
        response = self.client.get("/api/v1/transaction/count", params=query_param)
        return TypeAdapter(int).validate_json(response.content)

    def count_hubcheckouttrackers(self, **kwargs) -> int:
        query_param = {}
        response = self.client.get("/api/v1/checkout/tracker/count", params=query_param)
        return TypeAdapter(int).validate_json(response.content)

    def count_hubcheckouts(self, **kwargs) -> int:
        query_param = {}
        response = self.client.get("/api/v1/checkout/count", params=query_param)
        return TypeAdapter(int).validate_json(response.content)

    def query_items(self,
                    limit: int = 100,
                    offset: int = 0,
                    query_param: dict | None = None) -> list[dict]:
        query_param = {
            "limit": limit,
            "offset": offset,
            **query_param
        }
        response = self.client.get("/api/v1/item/wide", params=query_param)
        return self.handle_response(response=response, response_type=list[dict])

    def get_item_wide(self, item_identifier: str):
        response = self.client.get(f"/api/v1/item/wide/{item_identifier}")
        return self.handle_response(response=response, response_type=dict)
