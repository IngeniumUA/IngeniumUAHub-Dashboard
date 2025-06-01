import streamlit as st
import duckdb


@st.cache_resource
def duck_connection() -> duckdb.DuckDBPyConnection:
    """
    Global DuckDB Database connection
    """
    if "duck_conn" not in st.session_state:
        # If the application is running in production, we use an in memory database
        # When developing, to prevent populating the db on every change, we store in a file
        duck_url = "duck.duckdb"  # "duck.duckdb" if settings.is_debug() else ":memory:"

        # Configuration options
        # https://duckdb.org/docs/stable/configuration/overview.html#configuration-reference
        config = {}

        # Creating connection
        duck = duckdb.connect(database=duck_url, config=config)
        st.session_state["duck_conn"] = duck
    return st.session_state["duck_conn"]
