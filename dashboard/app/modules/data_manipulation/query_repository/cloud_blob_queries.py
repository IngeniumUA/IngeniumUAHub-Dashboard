import streamlit as st
import polars as pl

from app.page.cached_resources.duckdb_connection import duck_connection


def get_cloud_blob_count() -> int:
    stmt = """
    SELECT COUNT(*) FROM cloudblob
    """
    duck = duck_connection()
    return duck.execute(stmt).fetchone()[0]

@st.cache_data
def get_cloud_blob_df(limit: int) -> pl.DataFrame:
    stmt = """
    SELECT * FROM cloudblob LIMIT $limit
    """
    duck = duck_connection()
    return duck.execute(stmt, {"limit": limit}).pl()
