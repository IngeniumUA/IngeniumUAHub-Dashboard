import streamlit as st


@st.fragment
def order_tracking_analytics_page():
    # -----
    # Data Loading
    # -----

    # -----
    # Displaying
    # -----
    st.header("Order Tracking Analytics Page")
    with st.container(border=True) as configuration_container:
        configuration_container.subheader("Configuration")
        ingestion_col, _, _ = st.columns(3)

        ingestion_col.text("Ingestion")
        ingestion_col.toggle(
            label="Checkout Data",
            value=st.session_state.get("checkout_data_ingestion"),
            key="checkout_data_ingestion",
        )
        ingestion_col.toggle(
            label="Transaction Data",
            value=st.session_state.get("transaction_data_ingestion"),
            key="transaction_data_ingestion",
        )
        ingestion_col.toggle(
            label="Checkout Tracker Data",
            value=st.session_state.get("checkout_tracker_data_ingestion"),
            key="checkout_tracker_data_ingestion",
        )
    ingestion_col.toggle(
        label="Log data",
        value=st.session_state.get("log_data_ingestion"),
        key="log_data_ingestion",
    )

    with st.container(border=True):
        st.subheader("Summary Analytics")
        st.write("Refreshing every: ", 5)

    with st.container(border=True):
        st.subheader("Continuous groupby datetime")
        st.write("Refreshing every: ", 5)

    with st.container(border=True):
        st.subheader("Tracker Creation - completion delay")
