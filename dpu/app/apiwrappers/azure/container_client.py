from typing import Annotated, Optional, Literal

from azure.core.credentials import AzureNamedKeyCredential
from azure.storage.blob.aio import ContainerClient
from fastapi import Depends

from app.settings import settings


class AzureContainerClient:
    def __init__(self, account_name: str, container_key: str):
        self.account_name = account_name
        self.container_key: str = container_key

        self._credential: Optional[AzureNamedKeyCredential] = None

    @property
    def credential(self) -> AzureNamedKeyCredential:
        """
        Lazy evaluation -> Only initialised when required
        """
        if self._credential is None:
            self._credential = AzureNamedKeyCredential(
                self.account_name, self.container_key
            )
        return self._credential

    async def __call__(self, container_name: Literal["ingenium-cloud", "cloud-review"]) -> ContainerClient:
        """
        Creates a new connection instance for every request calling the dependency
        """
        url = f"https://{self.account_name}.blob.core.windows.net"
        container_client = ContainerClient(
            account_url=url,
            credential=self.credential,
            container_name=container_name,
        )
        try:
            yield container_client
        finally:
            await container_client.close()  # Ensures cleanup


AzureContainerDep = Annotated[ContainerClient, Depends(AzureContainerClient(account_name="ingeniumuacloud", container_key=settings.azure_storage_key))]
