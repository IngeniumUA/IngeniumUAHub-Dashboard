from fastapi import APIRouter
import polars as pl

from app.apiwrappers.hub.core_client import CoreClientDep
from app.modules.duckdb.duck_general_query_repository import DuckGeneralRepository
from app.modules.duckdb.duckdb_dep import DuckDBDep
from app.modules.exception.hubexception import HubException
from app.systems.ingestion.ingestion_interface import IngestionInterfaceDep

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

@duck_router.post("/table/{table_data}/sync")
async def sync_data(table_data: str,
                    core_client: CoreClientDep,
                    duck_connection: DuckDBDep,
                    ingestion_interface: IngestionInterfaceDep
                    ) -> bool:
    """
    Control API to launch a sync event
    """
    if table_data in ["hubcheckout", "hubtransaction", "hubcheckouttracker", "hubdblog"]:
        data_source = "core"
    else:
        raise HubException.invalid_argument(argument=table_data)

    await ingestion_interface.ingest(core_client=core_client,
                                     duck_connection=duck_connection,
                                     data_source=data_source,
                                     table_data=table_data)
    return True

@duck_router.get("/fetch_duck")
async def execute_query(stmt: str):
    """
    If the
    """
