import streamlit as st

from app.modules.duckdb.duckdb_connection import duck_connection


@st.cache_data
def get_transaction_count() -> int:
    stmt = """
    SELECT COUNT(*) FROM hubtransaction
    """
    duck = duck_connection()
    return duck.execute(stmt).fetchone()[0]
