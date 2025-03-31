import streamlit as st
import polars as pl
from io import StringIO

def load_in_csv_file():
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To convert to a string based IO:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

        column_type_mapping = {
            "name": pl.String,
            "id": pl.String,
            "email": pl.String,
            "price": pl.String,
            "validity": pl.String,
            "transaction_status": pl.String,
            "note": pl.String,
            "created_timestamp": pl.String,
            "blueprint_name": pl.String,
            "price_policy_name": pl.String,
            "purchased_product": pl.String,
        }
        raw_export_transaction = pl.scan_csv(stringio, separator=";", schema=column_type_mapping, has_header=True).collect()
        parsed_for_type_df = raw_export_transaction.with_columns(
            pl.col('id').str.to_integer(),
            pl.col('price').str.to_integer(),
            pl.col('created_timestamp').str.to_datetime(format="%Y-%m-%d %H:%M:%S%.f", strict=True) + pl.duration(hours=2)
        )
        return parsed_for_type_df
