import streamlit as st
import polars as pl
from pydantic import TypeAdapter

from app.page.cached_resources.clients import get_core_client

def lidkaarten_overview_old_page():
    st.title('Lidkaarten')

    core_client = get_core_client()
    response = core_client.client.get(f"api/v1/item/wide/card?limit=700")
    response_list = TypeAdapter(list[dict]).validate_python(response.json())
    source_df = pl.json_normalize(response_list, max_level=1)

    csv_bytes = source_df.write_csv().encode("utf-8")
    st.download_button(
        label="Download as CSV",
        data=csv_bytes,
        file_name="lidkaarten.csv",
        mime="text/csv",
    )

    st.dataframe(source_df)

