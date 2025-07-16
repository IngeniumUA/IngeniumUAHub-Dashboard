from typing import Annotated

from fastapi import Depends
from pydantic import TypeAdapter
from app.apiwrappers.hub.hub_client import HubClient
from app.settings import settings


class CoreClient(HubClient):
    async def internal_summarised(self):
        response = await self.client.get("/api/v1/internal/summarised")
        return TypeAdapter(dict[str, int]).validate_json(response.content)

    async def query_transactions(
        self, limit: int = 100, offset: int = 0, **kwargs
    ) -> list[dict]:
        query_param = dict(limit=limit, offset=offset)
        response = await self.client.get("/api/v1/transaction", params=query_param)
        return TypeAdapter(list[dict]).validate_json(response.content)

    async def query_hubcheckouttrackers(
        self, limit: int = 100, offset: int = 0, **kwargs
    ) -> list[dict]:
        query_param = dict(limit=limit, offset=offset)
        response = await self.client.get("/api/v1/checkout/tracker", params=query_param)
        return TypeAdapter(list[dict]).validate_json(response.content)

    async def query_hubcheckouts(
        self, limit: int = 100, offset: int = 0, **kwargs
    ) -> list[dict]:
        query_param = dict(limit=limit, offset=offset)
        response = await self.client.get("/api/v1/checkout", params=query_param)
        return self.handle_response(response=response, response_type=list[dict])

    async def count_transactions(self, **kwargs) -> int:
        query_param = {}
        response = await self.client.get("/api/v1/transaction/count", params=query_param)
        return TypeAdapter(int).validate_json(response.content)

    async def count_hubcheckouttrackers(self, **kwargs) -> int:
        query_param = {}
        response = await self.client.get("/api/v1/checkout/tracker/count", params=query_param)
        return TypeAdapter(int).validate_json(response.content)

    async def count_hubcheckouts(self, **kwargs) -> int:
        query_param = {}
        response = await self.client.get("/api/v1/checkout/count", params=query_param)
        return TypeAdapter(int).validate_json(response.content)

    async def query_items(self,
                    limit: int = 100,
                    offset: int = 0,
                    query_param: dict | None = None) -> list[dict]:
        query_param = {
            "limit": limit,
            "offset": offset,
            **(query_param if query_param else {})
        }
        response = await self.client.get("/api/v1/item/wide", params=query_param)
        return self.handle_response(response=response, response_type=list[dict])

    async def get_item_wide(self, item_identifier: str):
        response = await self.client.get(f"/api/v1/item/wide/{item_identifier}")
        return self.handle_response(response=response, response_type=dict)

    async def query_dblogs(self,
                     limit: int = 100,
                     offset: int = 0,
                     query_param: dict | None = None) -> list[dict]:
        query_param = {
            "limit": limit,
            "offset": offset,
            **(query_param if query_param else {})
        }
        response = await self.client.get("/api/v1/dblog", params=query_param)
        return self.handle_response(response=response, response_type=list[dict])

core_client = CoreClient(base_url=settings.core_api_url)

async def get_core_client():
    return core_client

CoreClientDep = Annotated[CoreClient, Depends(get_core_client)]
