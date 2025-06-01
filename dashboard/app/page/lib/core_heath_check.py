from typing import Optional

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from app.page.cached_resources.clients import get_core_client
from app.settings import settings

@st.fragment
def core_health_check(streamlit_container: Optional[DeltaGenerator]):
    core = get_core_client()

    # -----
    # Displaying
    if streamlit_container:
        streamlit_container.subheader("Core Health Check")
        streamlit_container.write(f"""server_url={settings.keycloak_server_url},
            client_id={settings.keycloak_client_id},
            realm_name={settings.keycloak_realm},
            client_secret_key={settings.keycloak_client_secret is not None and settings.keycloak_client_secret != ""}""")

    # Health check
    try:
        core_check = core.health_check()
        if streamlit_container:
            streamlit_container.markdown("#### Health Check")
            streamlit_container.write(core_check)
    except Exception as e:
        st.toast(f"Core Health Check Failed: {e}")

    # Auth check (for service)
    try:
        auth_check = core.health_check()
        if streamlit_container:
            streamlit_container.markdown("#### Core auth Check")
            streamlit_container.write(auth_check)
    except Exception as e:
        st.toast(f"Auth Check Failed: {e}")
