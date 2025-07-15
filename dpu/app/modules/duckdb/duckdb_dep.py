from typing import Annotated
import duckdb
from fastapi import Depends


async def duckdb_connection():
    return duckdb.connect(database=':memory:', read_only=False)


DuckDBDep = Annotated[duckdb.DuckDBPyConnection, Depends(duckdb_connection)]
