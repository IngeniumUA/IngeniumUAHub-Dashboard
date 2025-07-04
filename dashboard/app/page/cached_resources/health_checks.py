from datetime import timedelta

import streamlit as st

from app.page.cached_resources.clients import get_core_client, get_data_client, get_link_client, get_umami_client


@st.cache_data(ttl=timedelta(seconds=5))
def core_health_check() -> dict:
    client = get_core_client()
    response = client.health_check()

    status = "Ok" if response.status_code == 200 else "Error"
    return {
        "status": status,
        "status_code": response.status_code,
        "response_time": response.elapsed.microseconds / 1000,
    }

@st.cache_data(ttl=timedelta(seconds=5))
def core_internal_check() -> dict:
    client = get_core_client()
    return client.internal_summarised()

@st.cache_data(ttl=timedelta(seconds=5))
def data_health_check() -> dict:
    client = get_data_client()
    response = client.health_check()

    status = "Ok" if response.status_code == 200 else "Error"
    return {
        "status": status,
        "status_code": response.status_code,
        "response_time": response.elapsed.microseconds / 1000,
    }

@st.cache_data(ttl=timedelta(seconds=5))
def link_health_check() -> dict:
    client = get_link_client()
    response = client.health_check()

    status = "Ok" if response.status_code == 200 else "Error"
    return {
        "status": status,
        "status_code": response.status_code,
        "response_time": response.elapsed.microseconds / 1000,
    }

@st.cache_data(ttl=timedelta(seconds=5))
def traffic_health_check() -> dict:
    client = get_umami_client()
    response = client.health_check()

    status = "Ok" if response.status_code == 200 else "Error"
    return {
        "status": status,
        "status_code": response.status_code,
        "response_time": response.elapsed.microseconds / 1000,
    }

