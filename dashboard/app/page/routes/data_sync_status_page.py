import datetime

import streamlit as st

from app.modules.duckdb.duckdb_tables import duckdb_table_summary, table_counts

from app.page.cached_resources.clients import get_data_client

@st.fragment()
def dpu_db_status_fixture():
    with st.container(border=True):
        st.header("Duck Context")
        st.caption("Running DuckDB statistics")
        st.write(f"Updated {datetime.datetime.now(datetime.timezone.utc).time()}")
        st.markdown("### DPU Tables and Data sources")

        data_col, buttons_col = st.columns(2)
        dpu_client = get_data_client()
        tables_df = dpu_client.get_duckdb_content()
        data_col.dataframe(tables_df)

        buttons_col.caption("Core Data source")
        for col in ["HubTransaction", "HubCheckout", "HubCheckoutTracker"]:
            if buttons_col.button(label=col):
                if dpu_client.launch_sync_event(col.lower()):
                    st.toast(":green[Synced successfully]")
                else:
                    st.toast(":red[Failed to sync]")
                st.rerun()

@st.fragment()
def duck_db_status_fixture():
    with st.container(border=True):
        st.header("Duck Context")
        st.caption("Running DuckDB statistics")
        st.write(f"Updated {datetime.datetime.now(datetime.timezone.utc).time()}")

        st.markdown("### Tables and their statistics")
        tables_df = duckdb_table_summary()
        st.dataframe(tables_df.join(table_counts(tables_df["table_name"]), on="table_name"))


def data_sync_status_page():
    # -----
    st.title("Data Ingestion")
    st.caption(
        "Continuous monitoring tool for loading data from different services into duckdb for analytics."
        "Streamlit will only load data into own duckdb when the application is being used."
        "The database is global for everyone using this application"
    )

    # Own DuckDB Statistics
    duck_db_status_fixture()

    # DPU DuckDB Statistics
    dpu_db_status_fixture()

    #
    # with st.container(border=True):
    #     st.header("HubTransaction")
    #     st.caption("HubTransaction synced status")
    #
    #     is_table = table_exists(table_name="hubtransaction")
    #     in_table_txt = ":green[Yes]" if is_table else ":red[No]"
    #     st.write(f"Present in database: {in_table_txt}")
    #
    #     if is_table:
    #         trans_count = get_transaction_count()
    #         core_trans_count = core.count_transactions()
    #         st.write(f"{trans_count} out of {core_trans_count}")
    #
    # with st.container(border=True):
    #     st.header("HubCheckout")
    #     st.caption("HubCheckout synced status")
    #
    #     is_table = table_exists(table_name="hubcheckout")
    #     in_table_txt = ":green[Yes]" if is_table else ":red[No]"
    #     st.write(f"Present in database: {in_table_txt}")
    #
    #     if is_table:
    #         checkout_count = get_checkout_count()
    #         core_checkout_count = core.count_hubcheckouts()
    #         st.write(f"{checkout_count} out of {core_checkout_count}")
    #
    # with st.container(border=True):
    #     st.header("HubCheckoutTracker")
    #     st.caption("HubCheckoutTracker synced status")
    #
    #     is_table = table_exists(table_name="hubcheckouttracker")
    #     in_table_txt = ":green[Yes]" if is_table else ":red[No]"
    #     st.write(f"Present in database: {in_table_txt}")
    #
    #     if is_table:
    #         checkout_tracker_count = get_checkout_tracker_count()
    #         core_checkout_tracker_count = core.count_hubcheckouttrackers()
    #         st.write(f"{checkout_tracker_count} out of {core_checkout_tracker_count}")
    #
    # with st.container(border=True):
    #     st.header("Cloud Blobs")
    #     st.caption("Cloud Blobs synced status")
    #
    #     is_table = table_exists(table_name="cloudblob")
    #     in_table_txt = ":green[Yes]" if is_table else ":red[No]"
    #     st.write(f"Present in database: {in_table_txt}")
    #
    #     if is_table:
    #         cloud_client = get_azure_connection()
    #         cloud_blob_count = CloudSyncManager.fetch_data_count(cloud_client=cloud_client)
    #         cloud_duck_count = get_cloud_blob_count()
    #         st.write(f"{cloud_duck_count} out of {cloud_blob_count}")
    #
    #     st.button("Sync once", key="ingest_cloudblob_sync_once")
    #
    #     if is_table:
    #         st.dataframe(get_cloud_blob_df(limit=100))
