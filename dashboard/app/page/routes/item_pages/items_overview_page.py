import streamlit as st
import polars as pl

from app.page.cached_resources.clients import get_core_client


def fetch_items(query_param: dict):
    core_client = get_core_client()
    return core_client.query_items(query_param=query_param)

def items_overview_page():
    st.title('Items Overview')

    resp = fetch_items({})

    source_df = pl.json_normalize(resp, max_level=1)
    st.write(source_df)

    for row in source_df.select("item.id", "item.name").to_dicts():
        item_id = row["item.id"]
        name = row["item.name"]

        if st.button(f"View {name}", key=item_id):
            st.experimental_set_query_params(item=item_id)
            st.switch_page("Item Details")
