import streamlit as st

from app.apiwrappers.umami.umami_client import UmamiClient
from app.modules.core.core_api import CoreClient
from app.settings import settings


@st.cache_resource
def get_core_client():
    connection_timeout = 10.0 if settings.is_debug() else 3.0
    return CoreClient(
        base_url=settings.core_api_url, connection_timeout=connection_timeout
    )


@st.cache_resource
def get_umami_client() -> UmamiClient:
    return UmamiClient(
        username=settings.umami_username,
        password=settings.umami_password,
        base_url="https://traffic.ingeniumua.be",
        connection_timeout=3.0,
    )
