import streamlit as st
import polars as pl

from app.page.cached_resources.clients import get_core_client

def lidkaarten_overview_old_page():
    st.title('Lidkaarten')

    core_client = get_core_client()
    response = core_client.client.get("api/v1/item/wide/card?limit=1000")
    source_df = pl.json_normalize(response, max_level=1)
    st.dataframe(source_df)

