import streamlit as st

from app.settings import settings


def main_page():
    st.title("Main Page")
    if "keycloak_token" in st.session_state:
        st.write(st.session_state["keycloak_token"])

    # Showing config
    st.write(settings.model_dump())
