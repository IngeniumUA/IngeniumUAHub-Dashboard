from fastapi import APIRouter

from app.apiwrappers.azure.container_client import AzureContainerDep
from app.systems.ingestion.cloud_to_duckdb import CloudSyncManager

cloud_router = APIRouter(prefix="/cloud", tags=["v1"])

@cloud_router.get("/storage/count/{container_name}")
async def in_storage_count(container_client: AzureContainerDep,
                           name_starts_with: str = ""):
    return await CloudSyncManager.fetch_data_count(container_client=container_client, name_starts_with=name_starts_with)
