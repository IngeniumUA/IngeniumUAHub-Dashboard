from datetime import datetime

from azure.storage.blob.aio import ContainerClient
from duckdb.duckdb import DuckDBPyConnection

from app.apiwrappers.azure.container_client import AzureContainerClient

import polars as pl


class DPUStorage:
    """
    Documentation

    We want to:
    - Store tables
    - Know when a table was saved
    - What is in the table

    Constraints
    - To easily query everything we have to encode all the info in the filename
    - Parquet files (how we store the data) are best maxed between 100mb and 1gb

    So:
    - We keep a folder for every table
    - Encode the filename, the creation date and the row min and max index

    Example how that looks:
    hubtransaction >
        > 15-7-2025-10-03-10_100-901
        > hubtransaction_15-7-2025-10-03-10_100-901

    """

    @classmethod
    async def load_parquet(cls,
                           table_name: str,
                           azure_connection: ContainerClient):
        """

        """
        filenames = await azure_connection.list_blob_names(name_starts_with=table_name)
        if not filenames:
            return None

        parsed_filenames: list[tuple[str, datetime]] = list(
            sorted(map(lambda filename: cls._parse_filename(filename), filenames),
                   key=lambda pair: pair[1], reverse=True))
        most_recent_filename = parsed_filenames[0][0]  # First sorted, then filename from tuple
        if not most_recent_filename:
            return None

        blob = await azure_connection.download_blob(most_recent_filename)
        if blob is None:
            return None

        # todo load parquet into duckdb

    @classmethod
    def _table_to_filename(cls, table_name: str) -> str:
        """
        @param: table_name
        """
        ...

    @classmethod
    def _parse_filename(cls, filename: str) -> tuple[str, datetime]:
        """
        @param: filename
        """
        ...

    @classmethod
    async def store_df_as_parquet(cls,
                                  table_name: str,
                                  source_df: pl.DataFrame,
                                  azure_connection: AzureContainerClient):
        ...

    @classmethod
    async def store_table_as_parquet(cls,
                                     table_name: str,
                                     duck_connection: DuckDBPyConnection,
                                     azure_connection: AzureContainerClient):
        ...