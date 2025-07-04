import streamlit as st

from app.modules.hub.core_parsing import parse_dblogs_to_df, parse_dblogs_to_fields_denormalized_df
from app.page.cached_resources.clients import get_core_client


def dblog_page():
    st.title("DBLog Page")

    core_client = get_core_client()

    logs = core_client.query_dblogs(limit=100, offset=0)

    log_df = parse_dblogs_to_fields_denormalized_df(logs)

    st.dataframe(log_df)
