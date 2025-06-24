from typing import Optional, Literal

from pydantic import TypeAdapter

from app.modules.hub.hub_client import HubClient


class DataClient(HubClient):
    def get_azure_blob_count(self, container_name: Literal["ingenium-cloud", "cloud-review"], name_starts_with: Optional[str] = None):
        """
        Hacky method for one-of requests for which I'm to lazy to write a function
        """
        query_param = {}
        if name_starts_with:
            query_param["name_starts_with"] = name_starts_with

        response = self.client.get(f"/api/v1/cloud/storage/count/{container_name}", params=query_param)
        return TypeAdapter(int).validate_json(response.content)
