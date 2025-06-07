import streamlit as st

from app.apiwrappers.azure.container_client import AzureContainerClient
from app.settings import settings

@st.cache_resource(ttl=10)
def get_azure_connection():
    azure = AzureContainerClient(account_name="ingeniumuacloud",
                                 container_name="ingenium-cloud",
                                 container_key=settings.azure_storage_key)
    return azure()
