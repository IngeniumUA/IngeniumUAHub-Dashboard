from typing import Optional

from azure.core.credentials import AzureNamedKeyCredential
from azure.storage.blob import ContainerClient


class AzureContainerClient:
    def __init__(self, account_name: str, container_name: str, container_key: str):
        self.account_name = account_name
        self.container_name: str = container_name
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

    def __call__(self) -> ContainerClient:
        url = f"https://{self.account_name}.blob.core.windows.net"
        return ContainerClient(
            account_url=url,
            credential=self.credential,
            container_name=self.container_name,
        )

