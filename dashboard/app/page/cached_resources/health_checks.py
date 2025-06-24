from datetime import timedelta

import streamlit as st

from app.page.cached_resources.clients import get_core_client, get_data_client


@st.fragment(run_every=timedelta(seconds=5))
def core_health_check() -> dict:
    client = get_core_client()
    response = client.health_check()

    status = "Ok" if response.status_code == 200 else "Error"
    return {
        "status": status,
        "response_time": response.elapsed.microseconds,
    }

@st.fragment(run_every=timedelta(seconds=5))
def data_health_check() -> dict:
    client = get_data_client()
    response = client.health_check()

    status = "Ok" if response.status_code == 200 else "Error"
    return {
        "status": status,
        "response_time": response.elapsed.microseconds,
    }
