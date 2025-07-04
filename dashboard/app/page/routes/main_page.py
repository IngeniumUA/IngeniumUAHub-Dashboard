import streamlit as st
from pandas import Timedelta

from app.page.cached_resources.health_checks import core_health_check, data_health_check, core_internal_check, \
    link_health_check, traffic_health_check
from app.settings import settings


@st.fragment(run_every=Timedelta(seconds=5))
def health_checks_component():
    st.subheader("Service Health Checks")
    st.markdown("### Hub Services")

    core_col, data_col, link_col = st.columns(3)
    traffic_col, keycloak_col, wiki_col = st.columns(3)

    with core_col.container(border=True):
        st.markdown("#### Core API")
        st.caption(settings.core_api_url)

        health_check = core_health_check()
        if health_check["status"] == "Ok":
            st.markdown(f"### :green[Healthy {health_check["status_code"]}]")
        else:
            st.markdown(f"### :red[Unhealthy {health_check["status_code"]}]")
        st.caption(f"Response in {health_check["response_time"]} ms")

        internal = core_internal_check()
        event_loop_col, thread_pool_col = st.columns(2)
        event_loop_col.write(f"Event loop: :blue[{internal["running_tasks"]}] tasks")

        thread_pool_col.write(f"Using :blue[{internal["threads_in_use"]}] out of :blue[{internal["max_threads"]}] threads")

    with data_col.container(border=True):
        st.markdown("#### Data API")
        st.caption(settings.dpu_api_url)
        health_check = data_health_check()

        if health_check["status"] == "Ok":
            st.markdown(f"### :green[Healthy {health_check["status_code"]}]")
        else:
            st.markdown(f"### :red[Unhealthy {health_check["status_code"]}]")
        st.caption(f"Response in {health_check["response_time"]} ms")

    with link_col.container(border=True):
        st.markdown("#### Link Server")
        st.caption("https://li.ingeniumua.be")
        health_check = link_health_check()

        if health_check["status"] == "Ok":
            st.markdown(f"### :green[Healthy {health_check["status_code"]}]")
        else:
            st.markdown(f"### :red[Unhealthy {health_check["status_code"]}]")
        st.caption(f"Response in {health_check["response_time"]} ms")

    with traffic_col.container(border=True):
        st.markdown("#### Traffic")
        st.caption("https://traffic.ingeniumua.be")
        health_check = traffic_health_check()

        if health_check["status"] == "Ok":
            st.markdown(f"### :green[Healthy {health_check["status_code"]}]")
        else:
            st.markdown(f"### :red[Unhealthy {health_check["status_code"]}]")
        st.caption(f"Response in {health_check["response_time"]} ms")

    with keycloak_col.container(border=True):
        st.markdown("#### Keycloak")
        st.caption(settings.keycloak_server_url)

    with wiki_col.container(border=True):
        st.markdown("#### Wikipedia")
        st.caption("https://wiki.ingeniumua.be")


def main_page():
    st.title("Main Page")

    # -----
    # Display
    health_checks_component()

    # -----
    # Random things for debugging

    # if "keycloak_token" in st.session_state:
    #     st.write(st.session_state["keycloak_token"])
    # else:
    #     st.write("No keycloak token stored")
    #
    # # Showing config
    # st.write(settings.model_dump())
