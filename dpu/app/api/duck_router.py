from fastapi import APIRouter
import polars as pl

from app.modules.duckdb.duck_general_query_repository import DuckGeneralRepository
from app.modules.duckdb.duckdb_dep import DuckDBDep
from app.modules.exception.hubexception import HubException

duck_router = APIRouter(prefix="/sync", tags=["v1"])

@duck_router.get("/content")
async def get_duckdb_content(duck_connection: DuckDBDep) -> dict:
    return DuckGeneralRepository.table_summary(duck_connection=duck_connection).to_dict(as_series=False)

@duck_router.get("/source/content")
async def get_data_source_sync() -> dict:
    """
    Returns how much of core/cloud/umami data has been synchronised to the OLAP database
    """
    ...

@duck_router.get("/table/{data_table}/content")
async def get_data_count(data_table: str,
                         duck_connection: DuckDBDep):
    return DuckGeneralRepository.table_count(duck_connection=duck_connection, table=data_table).to_dict(as_series=False)

@duck_router.post("/table/{data_table}/sync")
async def sync_data(data_table: str) -> bool:
    """
    Control API to launch a sync event
    """
    if data_table in ["hubtransaction", "hubcheckout", "hubdblog", "hubcheckouttracker"]:
        # Core Sync
        ...
    elif data_table in []:
        # Umami sync
        ...
    else:
        raise HubException.resource_not_found(resource="data_table", identifier=data_table)
    return True

@duck_router.get("/fetch_duck")
async def execute_query(stmt: str):
    """
    If the
    """
