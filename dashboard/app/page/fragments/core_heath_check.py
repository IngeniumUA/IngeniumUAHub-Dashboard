import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from app.modules.core.core_api import CoreClient
from app.settings import settings


@st.cache_resource
def get_core_client():
    return CoreClient()

@st.fragment
def core_health_check(streamlit_container: DeltaGenerator):
    core = get_core_client()

    # -----
    # Displaying
    streamlit_container.subheader("Core Health Check")
    st.write(f"""server_url={settings.keycloak_server_url},
        client_id={settings.keycloak_client_id},
        realm_name={settings.keycloak_realm},
        client_secret_key={settings.keycloak_client_secret}"""
    )

    # Health check
    st.markdown("#### Health Check")
    st.write(core.health_check())

    # Auth check (for service)
    st.markdown("#### Core auth Check")
    st.write(core.auth_check())
