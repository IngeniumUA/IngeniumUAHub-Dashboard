from abc import abstractmethod
import polars as pl
from duckdb.duckdb import DuckDBPyConnection

from app.apiwrappers.hub.core_client import CoreClient
from app.modules.exception.hubexception import HubException
from app.modules.parsing.core_parsing import parse_checkouts_to_df, parse_checkouttrackers_to_df, \
    parse_transactions_to_df


class CoreSyncManager:
    def __init__(
        self,
        core_client: CoreClient,
        duck_connection: DuckDBPyConnection,
        table_name: str,
        allowed_total_requests: int = 200,
        max_objects_per_request: int = 500,
    ):
        self.core_client = core_client
        self.duck_connection = duck_connection

        self.table_name = table_name
        self.allowed_total_requests = allowed_total_requests
        self.max_objects_per_request = max_objects_per_request

    @abstractmethod
    async def fetch_data_count(self) -> int:
        return 0

    @abstractmethod
    async def fetch_data(
        self, limit: int, offset: int, **kwargs
    ) -> list[dict]:
        return []

    @abstractmethod
    def parse_to_df(self, input_list: list[dict], **kwargs):
        return pl.DataFrame()

    async def sync_once(self,
                        from_scratch: bool = False) -> bool:
        # -----
        # Fetch count
        count_in_core = await self.fetch_data_count()

        #
        # todo -> later on we can launch a couple separate requests async to combine?
        fetched_data: list[dict] = []
        for _ in range(self.allowed_total_requests):
            fetched_data += await self.fetch_data(
                limit=min(count_in_core, self.max_objects_per_request),
                offset=len(fetched_data),
            )
            if len(fetched_data) >= count_in_core:
                break
        else:
            raise HubException.internal_server_error()

        # -----
        # Parse to polars
        source_df = self.parse_to_df(fetched_data)

        # -----
        # Load into DB
        if from_scratch:
            stmt = (
                """SELECT COUNT(*) FROM duckdb_tables WHERE table_name = $table_name"""
            )
            result = self.duck_connection.execute(stmt, {"table_name": self.table_name}).fetchone()
            if result[0] > 0:  # If table exists (count > 0), drop it
                self.duck_connection.execute(f"DROP TABLE {self.table_name}")

        # Register the Polars DataFrame, then create
        self.duck_connection.register(f"temp_{self.table_name}_df", source_df)
        self.duck_connection.execute(
            f"CREATE TABLE {self.table_name} AS SELECT * FROM temp_{self.table_name}_df"
        )

        return True


class CoreSyncTransactionManager(CoreSyncManager):
    def __init__(self,
                 core_client: CoreClient,
                 duck_connection: DuckDBPyConnection,
                 ):
        super().__init__(core_client=core_client,
                         duck_connection=duck_connection,
                         table_name="hubtransaction")

    async def fetch_data_count(self) -> int:
        return await self.core_client.count_transactions()

    async def fetch_data(
        self, limit: int, offset: int, **kwargs
    ) -> list[dict]:
        return await self.core_client.query_transactions(limit=limit, offset=offset)

    def parse_to_df(self, input_list: list[dict], **kwargs):
        return parse_transactions_to_df(input_list)


class CoreSyncCheckoutManager(CoreSyncManager):
    def __init__(self,
                 core_client: CoreClient,
                 duck_connection: DuckDBPyConnection,
                 ):
        super().__init__(core_client=core_client,
                         duck_connection=duck_connection,
                         table_name="hubcheckout")

    async def fetch_data_count(self) -> int:
        return await self.core_client.count_hubcheckouts()

    async def fetch_data(
        self, limit: int, offset: int, **kwargs
    ) -> list[dict]:
        return await self.core_client.query_hubcheckouts(limit=limit, offset=offset)

    def parse_to_df(self, input_list: list[dict], **kwargs):
        return parse_checkouts_to_df(input_list)


class CoreSyncCheckoutTrackerManager(CoreSyncManager):
    def __init__(self,
                 core_client: CoreClient,
                 duck_connection: DuckDBPyConnection,
                 ):
        super().__init__(core_client=core_client,
                         duck_connection=duck_connection,
                         table_name="hubcheckouttracker")

    async def fetch_data_count(self) -> int:
        return await self.core_client.count_hubcheckouttrackers()

    async def fetch_data(
        self, limit: int, offset: int, **kwargs
    ) -> list[dict]:
        return await self.core_client.query_hubcheckouttrackers(limit=limit, offset=offset)

    def parse_to_df(self, input_list: list[dict], **kwargs):
        return parse_checkouttrackers_to_df(input_list)
