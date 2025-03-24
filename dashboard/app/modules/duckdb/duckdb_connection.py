import streamlit as st
import duckdb

@st.cache_resource
def duck_connection() -> duckdb.DuckDBPyConnection:
    if "duck_conn" not in st.session_state:
        duck = duckdb.connect("duck_explaining.duckdb")  # TODO Align with the rest of the app (use same duck)

        # TODO Check if duckdb is correctly initialised? -> Check if tables exist, etc

        st.session_state["duck_conn"] = duck
    return st.session_state["duck_conn"]
