import streamlit as st

from app.modules.duckdb.duckdb_connection import duck_connection


@st.cache_data
def get_checkout_count() -> int:
    stmt = """
    SELECT COUNT(*) FROM hubcheckout
    """
    duck = duck_connection()
    return duck.execute(stmt).fetchone()[0]
