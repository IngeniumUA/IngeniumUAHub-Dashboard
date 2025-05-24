import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import polars as pl

from plotly.subplots import make_subplots
import plotly.graph_objects as pgo


def transaction_analytics(container: DeltaGenerator, dataframe: pl.DataFrame, key: str):
    if dataframe.is_empty():
        container.warning("Input dataframe is empty")
        return

    time_interval_key = key + "_time_interval_key"
    options = (("5m", "30m", "1h", "1d"),)
    time_interval = container.selectbox(
        label="Select time interval",
        options=options,
        key=time_interval_key,
        index=options.index(
            st.session_state.get(time_interval_key, options[len(options) // 2])
        ),  # Default to middle
    )

    #
    per_timestamp = (
        dataframe.group_by(pl.col("created_timestamp").dt.round(time_interval))
        .agg(
            pl.col("id").count().alias("transaction_count"),
        )
        .sort("created_timestamp")
    )
    #
    per_product_blueprint = (
        dataframe.group_by(pl.col("blueprint_name"))
        .agg(
            pl.col("id").count().alias("transaction_count"),
        )
        .sort("transaction_count")
    )

    fig = make_subplots(
        1,
        2,
        x_title=f"Bestellingen per {time_interval}, alle dagen",
        subplot_titles=["Orders (n) as f of t"],
    )
    fig.add_trace(
        pgo.Scatter(
            x=per_timestamp["created_timestamp"],
            y=per_timestamp["transaction_count"],
            mode="lines+markers",
            name=f"Orders per {time_interval}",
            fill="tozeroy",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        pgo.Bar(
            name="Bestellingen per product",
            x=per_product_blueprint["blueprint_name"],
            y=per_product_blueprint["transaction_count"],
            text=per_product_blueprint["transaction_count"],  # Display values
            textposition="auto",  # Automatically position the text
        ),
        row=1,
        col=2,
    )
    container.plotly_chart(fig)


def transaction_analytics_page():
    dataframe = pl.DataFrame()

    container = st.container()
    transaction_analytics(container=container, dataframe=dataframe, key="ordertracking")
