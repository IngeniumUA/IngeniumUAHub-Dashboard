import asyncio
from typing import Annotated, Literal

from duckdb.duckdb import DuckDBPyConnection
from fastapi import Depends

from app.apiwrappers.hub.core_client import CoreClient
from app.modules.exception.hubexception import HubException
from app.systems.ingestion.core_ingestion import CoreSyncTransactionManager, CoreSyncCheckoutManager, \
    CoreSyncCheckoutTrackerManager


class IngestionInterface:
    def __init__(self):
        self.locks = {}

    def _get_lock(self, data_source_id: str):
        """
        To make sure two requests can't trigger a data source being filled at the same time
        We create a process-level lock.
        In the future we can replace this with aioredlock package once the redis is up
        """
        if data_source_id not in self.locks:
            self.locks[data_source_id] = asyncio.Lock()
        return self.locks[data_source_id]

    async def ingest(self,
                                 core_client: CoreClient,
                                 duck_connection: DuckDBPyConnection,
                                 data_source: Literal["core", "umami"],
                                 table_data: str):
        lock = self._get_lock(data_source + table_data)
        if lock.locked():
            raise HubException.already_syncing(data_source=data_source, table_name=table_data)

        async with lock:
            match data_source:
                case "core":
                    await self._core_ingestion(table_data=table_data,
                                               core_client=core_client,
                                               duck_connection=duck_connection)
                case _:
                    raise HubException.invalid_argument(argument=data_source)

    @classmethod
    async def _core_ingestion(cls,
                              table_data: str,
                              core_client: CoreClient,
                              duck_connection: DuckDBPyConnection,
                              from_scratch: bool = True
                              ):
        # Get the right syncmanager for core
        match table_data.lower(): # Lower just to make sure we don't allow funny case-sensitivity
            case "hubtransaction":
                sync_manager = CoreSyncTransactionManager(core_client=core_client,
                                                          duck_connection=duck_connection)
            case "hubcheckout":
                sync_manager = CoreSyncCheckoutManager(core_client=core_client,
                                                       duck_connection=duck_connection)
            case "hubcheckouttracker":
                sync_manager = CoreSyncCheckoutTrackerManager(core_client=core_client,
                                                              duck_connection=duck_connection)
            case "hubdblog":
                raise HubException.not_implemented()
            case _:
                raise HubException.invalid_argument(argument=table_data)

        # ----
        # Syncing
        await sync_manager.sync_once(from_scratch=from_scratch)


ingestion_interface = IngestionInterface()
async def get_ingestion_interface():
    return ingestion_interface

IngestionInterfaceDep = Annotated[IngestionInterface, Depends(get_ingestion_interface)]
