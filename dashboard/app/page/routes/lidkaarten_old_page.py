import streamlit as st
import polars as pl
from pydantic import TypeAdapter

from app.page.cached_resources.clients import get_core_client

def lidkaarten_overview_old_page():
    st.title('Lidkaarten')

    core_client = get_core_client()
    gathered_response = []
    with st.status("Loading .."):
        for i in range(0, 700//50):
            st.write(i)
            try:
                response = core_client.client.get(f"api/v1/item/wide/card?limit=50&offset={i*50}")
                response_list = TypeAdapter(list[dict]).validate_json(response.json())
                gathered_response.extend(response_list)
            except Exception as e:
                st.error(e)
                return
    source_df = pl.json_normalize(gathered_response, max_level=1)
    st.dataframe(source_df)

