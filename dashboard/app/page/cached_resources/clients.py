import streamlit as st

from app.modules.core.core_api import CoreClient


@st.cache_resource
def get_core_client():
    return CoreClient()
