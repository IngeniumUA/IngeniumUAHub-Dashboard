import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import polars as pl

from plotly.subplots import make_subplots
import plotly.graph_objects as pgo

from app.modules.core.core_parsing import parse_transactions_to_df
from app.page.colors import HEX_COLORS
from app.page.fragments.core_heath_check import get_core_client


def transaction_analytics(container: DeltaGenerator, dataframe: pl.DataFrame, key: str):
    if dataframe.is_empty():
        container.warning("Input dataframe is empty")
        return

    time_interval_key = key + "_time_interval_key"
    options = ("5m", "30m", "1h", "1d")

    time_interval = container.selectbox(
        label="Select time interval",
        options=options,
        key=time_interval_key,
        index=(len(options) // 2), # Default to middle
    )

    #
    per_created_timestamp = (
        dataframe.group_by(pl.col("created_timestamp").dt.round(time_interval))
        .agg(
            pl.col("interaction_id").count().alias("transaction_count"),
        )
        .sort("created_timestamp")
    )
    per_completed_timestamp = (
        dataframe.filter(pl.col("completed_timestamp").is_not_null()).group_by(pl.col("completed_timestamp").dt.round(time_interval))
        .agg(
            pl.col("interaction_id").count().alias("transaction_count"),
        )
        .sort("completed_timestamp")
    )
    #
    per_product_blueprint = (
        dataframe.group_by(pl.col("product_blueprint_name"))
        .agg(
            pl.col("interaction_id").count().alias("transaction_count"),
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
            x=per_created_timestamp["created_timestamp"],
            y=per_created_timestamp["transaction_count"],
            mode="lines+markers",
            name=f"Created Transactions per {time_interval}",
            marker=dict(color=HEX_COLORS["ingenium_purple"]),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        pgo.Scatter(
            x=per_completed_timestamp["completed_timestamp"],
            y=per_completed_timestamp["transaction_count"],
            mode="lines+markers",
            name=f"Completed Transactions per {time_interval}",
            marker=dict(color=HEX_COLORS["ingenium_blue"]),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        pgo.Bar(
            name="Bestellingen per product",
            x=per_product_blueprint["product_blueprint_name"],
            y=per_product_blueprint["transaction_count"],
            text=per_product_blueprint["transaction_count"],  # Display values
            textposition="auto",  # Automatically position the text
            marker=dict(color=HEX_COLORS["ingenium_blue"]),
        ),
        row=1,
        col=2,
    )
    container.plotly_chart(fig)


def transaction_analytics_page():
    core = get_core_client()

    # Fetching and parsing
    transactions = core.query_transactions()
    df = parse_transactions_to_df(transactions)

    # Displaying
    container = st.container()
    transaction_analytics(container=container, dataframe=df, key="transaction_overview")
