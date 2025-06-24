import streamlit as st

from app.modules.hub.core_client import CoreClient
from app.modules.hub.data_client import DataClient
from app.settings import settings


@st.cache_resource
def get_core_client():
    connection_timeout = 30.0 if settings.is_debug() else 3.0
    return CoreClient(
        base_url=settings.core_api_url, connection_timeout=connection_timeout
    )

@st.cache_resource
def get_data_client():
    connection_timeout = 30.0 if settings.is_debug() else 3.0
    return DataClient(
        base_url="http://ingeniumuahub-dashboard-data_processing-1:8000", connection_timeout=connection_timeout
    )
