import streamlit as st

from app.modules.authentication.authentication import authenticate_user_component
from app.page.fragments.core_heath_check import core_health_check
from app.settings import settings


def main_page():
    st.title("Main Page")

    # -----
    # Display
    core_check_container = st.container()
    core_health_check(streamlit_container=core_check_container)  # Core health check
    authenticate_user_component()  # Authentication on user-level

    #
    if "keycloak_token" in st.session_state:
        st.write(st.session_state["keycloak_token"])
    else:
        st.write("No keycloak token stored")

    # Showing config
    st.write(settings.model_dump())

    # Core API
    # core_client = CoreClient("dev_backendapiaccess", "")
    # core_client._keycloak_access_token()
    #
    # headers = {'authorization': f"Bearer {core_client.keycloak_token["access_token"]}"}
    # params = {}
    # with httpx.Client(headers=headers, params=params, base_url=settings.core_api_url) as client:
    #     response = client.get(url="user", headers=headers)
    #     st.write(response.status_code)
    #     st.write(response.text)
    #     st.write(response.content)
