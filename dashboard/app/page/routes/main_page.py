import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from app.page.cached_resources.health_checks import core_health_check, data_health_check


def health_checks_component(container: DeltaGenerator):
    container.subheader("Service Health Checks")
    container.markdown("### Hub Services")

    core_col, data_col, link_col = container.columns(3)
    traffic_col, keycloak_col, wiki_col = container.columns(3)

    with core_col.container(border=True):
        st.markdown("#### Core API")
        health_check = core_health_check()
        if health_check["status"] == "Ok":
            st.markdown("### :green[Healthy]")
        else:
            st.markdown("### :red[Unhealthy]")
        st.caption(f"Response in {health_check["response_time"]} ms")

    with data_col.container(border=True):
        st.markdown("#### Data API")
        health_check = data_health_check()

        if health_check["status"] == "Ok":
            st.markdown("### :green[Healthy]")
        else:
            st.markdown("### :red[Unhealthy]")
        st.caption(f"Response in {health_check["response_time"]} ms")

    with link_col.container(border=True):
        st.markdown("#### Link Server")

    with traffic_col.container(border=True):
        st.markdown("#### Traffic")

    with keycloak_col.container(border=True):
        st.markdown("#### Keycloak")

    with wiki_col.container(border=True):
        st.markdown("#### Wikipedia")


def main_page():
    st.title("Main Page")

    # -----
    # Display
    health_checks = st.container(border=True)
    health_checks_component(health_checks)

    # -----
    # Random things for debugging

    # if "keycloak_token" in st.session_state:
    #     st.write(st.session_state["keycloak_token"])
    # else:
    #     st.write("No keycloak token stored")
    #
    # # Showing config
    # st.write(settings.model_dump())
