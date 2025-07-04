import datetime
from typing import Literal, Iterable

import polars as pl
import streamlit as st

from app.page.cached_resources.duck import duck_connection

TRANS_TABLE = "hubtransaction"
CHECK_TABLE = "hubcheckout"
CHECK_TRACK_TABLE = "hubcheckouttransaction"


@st.cache_resource(ttl=datetime.timedelta(seconds=5))
def duckdb_table_summary() -> pl.DataFrame:
    stmt = """
    SELECT
        table_name,
        table_type
    FROM information_schema.tables
    WHERE table_schema = 'main'
    ORDER BY table_name
    """
    duck = duck_connection()
    return duck.execute(stmt).pl()

def table_counts(tables: Iterable[str]): # -> dict[str, int]:
    stmt = """"""
    for table in tables:
        stmt += f"SELECT '{table}' AS table_name, COUNT(*) AS row_count FROM {table} UNION ALL "

    # Guard clause behind the select (because Iterable[str] doesn't allow len()
    if stmt == "":
        return

    stmt = stmt[:-10]  # Stripping off last "UNION ALL"

    return duck_connection().execute(stmt).pl()

def table_exists(
    table_name: Literal["hubtransaction", "hubcheckout", "hubcheckouttracker", "cloudblob"],
) -> bool:
    return table_name in duckdb_table_summary()["table_name"].to_list()
