from typing import Iterable

import polars as pl
from duckdb.duckdb import DuckDBPyConnection


class DuckGeneralRepository:
    @classmethod
    def duckdb_table_summary(cls, duck_connection: DuckDBPyConnection) -> pl.DataFrame:
        stmt = """
        SELECT
            table_name,
            table_type
        FROM information_schema.tables
        WHERE table_schema = 'main'
        ORDER BY table_name
        """
        return duck_connection.execute(stmt).pl()

    @classmethod
    def table_count(cls, duck_connection: DuckDBPyConnection, table: str) -> pl.DataFrame:
        stmt = f"SELECT '{table}' AS table_name, COUNT(*) AS row_count FROM {table}"
        return duck_connection.execute(stmt).pl()

    @classmethod
    def table_counts(cls,
                     duck_connection: DuckDBPyConnection,
                     tables: Iterable[str]):  # -> dict[str, int]:
        stmt = """"""
        for table in tables:
            stmt += f"SELECT '{table}' AS table_name, COUNT(*) AS row_count FROM {table} UNION ALL "

        # Guard clause behind the select (because Iterable[str] doesn't allow len()
        if stmt == "":
            return

        stmt = stmt[:-10]  # Stripping off last "UNION ALL"

        return duck_connection.execute(stmt).pl()

    @classmethod
    def table_summary(cls, duck_connection: DuckDBPyConnection):
        tables_df: pl.DataFrame = cls.duckdb_table_summary(duck_connection)
        counts_df: pl.DataFrame =  cls.table_counts(duck_connection, tables_df["table_name"])

        if not counts_df.is_empty():
            tables_df = tables_df.join(
                counts_df, on="table_name", how="left"
            )
        return tables_df
