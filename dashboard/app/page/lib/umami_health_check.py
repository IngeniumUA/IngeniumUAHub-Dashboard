from typing import Optional

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from app.page.cached_resources.clients import get_umami_client
from app.settings import settings


@st.fragment
def umami_health_check(streamlit_container: Optional[DeltaGenerator]):
    umami_client = get_umami_client()

    # -----
    # Displaying
    if streamlit_container:
        streamlit_container.subheader("Umami Health Check")
        if settings.is_debug():
            st.warning("Umami client not available in local environment")
            return

    # Health check
    try:
        umami_check = umami_client.health_check()
        if streamlit_container:
            streamlit_container.markdown("#### Health Check")
            streamlit_container.write(umami_check)
    except Exception as e:
        st.toast(f"Umami Health Check Failed: {e}")

    # Auth check (for service)
    try:
        auth_check = umami_client.health_check()
        if streamlit_container:
            streamlit_container.markdown("#### Umami auth Check")
            streamlit_container.write(auth_check)
    except Exception as e:
        st.toast(f"Auth Check Failed: {e}")
