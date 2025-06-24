import streamlit as st

def duckdb_ingestion_analytics():
    tables = ("HubTransaction", "HubCheckout", "HubCheckoutTracker")

    with st.container(border=True):
        st.header("Core")
        return
        for table_name, col in zip(tables, st.columns(len(tables)), strict=False):
            with col.container(border=True):
                st.markdown(f"#### {table_name}")

                #
                in_db = table_exists(table_name=table_name.lower())
                in_db_txt = ":green[Yes]" if in_db else ":red[No]"
                st.write(f"Present in database: {in_db_txt}")

                #
                st.write("Automatic Sync")
                toggle_key = f"ingest_{table_name.lower()}"
                st.toggle(
                    key=toggle_key,
                    label="Enable auto sync",
                    value=st.session_state.get(toggle_key, False),
                )

                #
                st.button("Sync once", key=toggle_key + "_sync_once")


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
        "Continuous monitoring tool for loading data from different services into duckdb for analytics"
    )

    # # DuckDB Statistics
    # duck_db_status_fixture()
    #
    # # Ingestion configuration
    # duckdb_ingestion_analytics()  # General overview
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
