import streamlit as st

from app.page.lib.core_heath_check import core_health_check
from app.settings import settings


def main_page():
    st.title("Main Page")

    # -----
    # Display
    core_check_container = st.container()
    core_health_check(streamlit_container=core_check_container)  # Core health check

    if "keycloak_token" in st.session_state:
        st.write(st.session_state["keycloak_token"])
    else:
        st.write("No keycloak token stored")

    # Showing config
    st.write(settings.model_dump())
