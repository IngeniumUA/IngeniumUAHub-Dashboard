import datetime

import streamlit as st

from app.modules.duckdb.duckdb_tables import duckdb_table_summary, table_counts


@st.fragment(run_every=datetime.timedelta(seconds=5))
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
    # Data ingestion
    # fixme this should be moved to a global component
    if st.session_state.get("ingest_hubtransaction_sync_once", False):
        ...
    if st.session_state.get("ingest_hubcheckout_sync_once", False):
        ...
    if st.session_state.get("ingest_hubcheckouttracker_sync_once", False):
        ...
    if st.session_state.get("ingest_cloudblob_sync_once", False):
        ...

    # -----
    st.title("Data Ingestion")
    st.caption(
        "Continuous monitoring tool for loading data from different services into duckdb for analytics."
        "Streamlit will only load data into duckdb when the application is being used."
        "The database is global for everyone"
    )

    # # DuckDB Statistics
    duck_db_status_fixture()
    #

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
