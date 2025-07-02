import streamlit as st

from app.modules.hub.core_client import CoreClient
from app.modules.hub.data_client import DataClient
from app.modules.hub.link_client import LinkClient
from app.modules.hub.umami_client import UmamiClient
from app.settings import settings


@st.cache_resource
def get_core_client():
    connection_timeout = 30.0 if settings.is_debug() else 3.0
    return CoreClient(
        base_url=settings.core_api_url, connection_timeout=connection_timeout
    )

@st.cache_resource
def get_data_client() -> DataClient:
    connection_timeout = 30.0 if settings.is_debug() else 3.0
    return DataClient(
        base_url="http://ingeniumuahub-dashboard-data_processing-1:8000", connection_timeout=connection_timeout
    )

@st.cache_resource
def get_umami_client() -> UmamiClient:
    return UmamiClient(
        username=settings.umami_username,
        password=settings.umami_password,
        base_url="https://traffic.ingeniumua.be",
        connection_timeout=3.0,
    )

@st.cache_resource
def get_link_client() -> LinkClient:
    connection_timeout = 30.0 if settings.is_debug() else 3.0
    return LinkClient(
        base_url="https://li.ingeniumua.be", connection_timeout=connection_timeout
    )
