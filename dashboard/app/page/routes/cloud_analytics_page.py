import streamlit as st
from azure.storage.blob import ContainerClient

from app.page.cached_resources.azure_connection import get_azure_connection


def cloud_detail_page():
    st.title('Cloud Analytics Page')

    cloud_client: ContainerClient = get_azure_connection()

    st.subheader("Container properties")
    st.write(dict(cloud_client.get_container_properties()))

    # st.write(blob for blob in cloud_client.list_blob_names())
