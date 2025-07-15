import streamlit as st

from app.page.cached_resources.duckdb_connection import duck_connection


@st.cache_data
def get_checkout_tracker_count() -> int:
    stmt = """
    SELECT COUNT(*) FROM hubcheckouttracker
    """
    duck = duck_connection()
    return duck.execute(stmt).fetchone()[0]
