import datetime

import streamlit as st
import polars as pl

from app.modules.duckdb.duckdb_connection import duck_connection
from app.modules.duckdb.transaction.transaction_queries import get_transaction_count
from app.page.fragments.core_heath_check import get_core_client
from app.systems.ingestion.core_to_duckdb import CoreSyncTransactionManager


@st.cache_resource(ttl=datetime.timedelta(seconds=15))
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
    return duck.execute(stmt).df()

@st.fragment(run_every=datetime.timedelta(seconds=5))
def duck_db_status_fixture():
    with st.container(border=True):
        st.header("Duck Context")
        st.caption("Running DuckDB statistics")
        st.write(f"Updated {datetime.datetime.now(datetime.timezone.utc).time()}")

        st.markdown("### Tables and their statistics")
        st.dataframe(duckdb_table_summary())

def duckdb_ingestion_analytics():
    tables = ("HubTransaction", "HubCheckout", "HubCheckoutTracker")

    with st.container(border=True):
        for table_name, col in zip(tables, st.columns(len(tables))):
            with col.container(border=True):
                st.markdown(f"#### {table_name}")

                #
                in_db = table_name in duckdb_table_summary()["table_name"].to_list()
                in_db_txt = ":green[Yes]" if in_db else ":red[No]"
                st.write(f"Present in database: {in_db_txt}")

                #
                st.write(f"Automatic Sync")
                toggle_key = f"ingest_{table_name}"
                st.toggle(key=toggle_key, label="Enable auto sync", value=st.session_state.get(toggle_key, False))
                toggle_key_time = toggle_key + "_time"

                #
                sync_table = st.button("Sync once", key=toggle_key + "_sync_once")
                if sync_table:
                    CoreSyncTransactionManager.sync_once(from_scratch=True)


def duck_ingestion_page():
    core = get_core_client()

    # -----
    st.title("Data Ingestion")
    st.caption("Continuous monitoring tool for loading data from different services into duckdb for analytics")

    # DuckDB Statistics
    duck_db_status_fixture()

    # Ingestion configuration
    duckdb_ingestion_analytics()  # General overview

    with st.container(border=True):
        st.header("HubTransaction")
        st.caption("HubTransaction synced status")

        trans_count = get_transaction_count()
        core_trans_count = core.count_transactions()
        st.write(f"{trans_count} out of {core_trans_count}")
