from abc import abstractmethod
import polars as pl
import streamlit as st

from app.modules.core.core_api import CoreClient
from app.modules.core.core_parsing import (
    parse_transactions_to_df,
    parse_checkouttrackers_to_df,
    parse_checkouts_to_df,
)
from app.page.cached_resources.duckdb_connection import duck_connection
from app.page.cached_resources.clients import get_core_client


class CoreSyncManager:
    def __init__(
        self,
        table_name: str,
        allowed_total_requests: int = 10,
        max_objects_per_request: int = 100,
    ):
        self.table_name = table_name
        self.allowed_total_requests = allowed_total_requests
        self.max_objects_per_request = max_objects_per_request

    @abstractmethod
    def fetch_data_count(self, core_client: CoreClient) -> int:
        return 0

    @abstractmethod
    def fetch_data(
        self, core_client: CoreClient, limit: int, offset: int, **kwargs
    ) -> list[dict]:
        return []

    @abstractmethod
    def parse_to_df(self, input_list: list[dict], **kwargs):
        return pl.DataFrame()

    def sync_once(self, from_scratch: bool = False) -> bool:
        duck = duck_connection()
        core_client = get_core_client()

        # -----
        # Fetch count
        count_in_core = self.fetch_data_count(core_client=core_client)

        #
        # todo -> later on we can launch a couple separate requests async to combine?
        fetched_data: list[dict] = []
        for _ in range(self.allowed_total_requests):
            fetched_data += self.fetch_data(
                core_client=core_client,
                limit=min(count_in_core, self.max_objects_per_request),
                offset=len(fetched_data),
            )
            if len(fetched_data) >= count_in_core:
                break
        else:
            # fixme: this will also trigger if it needed exactly this amount of requests
            st.toast(
                f"Could not sync {self.table_name} in {self.allowed_total_requests} requests"
            )

        # -----
        # Parse to polars
        source_df = self.parse_to_df(fetched_data)

        # -----
        # Load into DB
        if from_scratch:
            stmt = (
                """SELECT COUNT(*) FROM duckdb_tables WHERE table_name = $table_name"""
            )
            result = duck.execute(stmt, {"table_name": self.table_name}).fetchone()
            if result[0] > 0:  # If table exists (count > 0), drop it
                duck.execute(f"DROP TABLE {self.table_name}")

        # Register the Polars DataFrame, then create
        duck.register(f"temp_{self.table_name}_df", source_df)
        duck.execute(
            f"CREATE TABLE {self.table_name} AS SELECT * FROM temp_{self.table_name}_df"
        )

        return True


class CoreSyncTransactionManager(CoreSyncManager):
    def __init__(self):
        super().__init__("hubtransaction")

    def fetch_data_count(self, core_client: CoreClient) -> int:
        return core_client.count_transactions()

    def fetch_data(
        self, core_client: CoreClient, limit: int, offset: int, **kwargs
    ) -> list[dict]:
        return core_client.query_transactions(limit=limit, offset=offset)

    def parse_to_df(self, input_list: list[dict], **kwargs):
        return parse_transactions_to_df(input_list)


class CoreSyncCheckoutManager(CoreSyncManager):
    def __init__(self):
        super().__init__("hubcheckout")

    def fetch_data_count(self, core_client: CoreClient) -> int:
        return core_client.count_hubcheckouts()

    def fetch_data(
        self, core_client: CoreClient, limit: int, offset: int, **kwargs
    ) -> list[dict]:
        return core_client.query_hubcheckouts(limit=limit, offset=offset)

    def parse_to_df(self, input_list: list[dict], **kwargs):
        return parse_checkouts_to_df(input_list)


class CoreSyncCheckoutTrackerManager(CoreSyncManager):
    def __init__(self):
        super().__init__("hubcheckouttracker")

    def fetch_data_count(self, core_client: CoreClient) -> int:
        return core_client.count_hubcheckouttrackers()

    def fetch_data(
        self, core_client: CoreClient, limit: int, offset: int, **kwargs
    ) -> list[dict]:
        return core_client.query_hubcheckouttrackers(limit=limit, offset=offset)

    def parse_to_df(self, input_list: list[dict], **kwargs):
        return parse_checkouttrackers_to_df(input_list)
