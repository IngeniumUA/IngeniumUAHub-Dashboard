import streamlit as st
from app.page.cached_resources.clients import get_data_client


def cloud_detail_page():
    st.title('Cloud Analytics Page')

    data_client = get_data_client()

    st.subheader("Main container")
    blob_count = data_client.get_azure_blob_count(container_name="ingenium-cloud")
    st.write(f"Holds :blue[{blob_count}] file blobs in container")


    st.subheader("Review container")
    blob_count = data_client.get_azure_blob_count(container_name="cloud-review")
    st.write(f"Holds :blue[{blob_count}] file blobs in container")
