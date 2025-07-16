from typing import Annotated
import duckdb
from fastapi import Depends


async def duckdb_connection():
    # Configuration options
    # https://duckdb.org/docs/stable/configuration/overview.html#configuration-reference
    config = {}

    return duckdb.connect(database='duck.duckdb',
                          read_only=False,
                          config=config)


DuckDBDep = Annotated[duckdb.DuckDBPyConnection, Depends(duckdb_connection)]
