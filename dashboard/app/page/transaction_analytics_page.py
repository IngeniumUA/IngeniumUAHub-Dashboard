import streamlit as st
import polars as pl

from plotly.subplots import make_subplots
import plotly.graph_objects as pgo

from app.systems.ingestion.csv_files import load_in_csv_file

def transaction_analytics():
    source_df = st.session_state.get('source_df', None)
    if source_df is None:
        st.session_state.source_df = load_in_csv_file()
        return

    time_interval = st.selectbox(
        "Selecteer tijdsinterval",
        ('5m', '30m', '1h', '1d'),
        placeholder="Select contact method...",
    )

    per_timestamp = source_df.group_by(
        pl.col('created_timestamp').dt.round(time_interval)
    ).agg(
        pl.col('id').count().alias('transaction_count'),
    ).sort(
        'created_timestamp'
    )
    per_product_blueprint = source_df.group_by(
        pl.col('blueprint_name')
    ).agg(
        pl.col('id').count().alias('transaction_count'),
    ).sort(
        'transaction_count'
    )

    fig = make_subplots(1, 2,
                        x_title=f"Bestellingen per {time_interval}, alle dagen",
                        subplot_titles=["Orders (n) as f of t"])

    fig.add_trace(
        pgo.Scatter(x=per_timestamp["created_timestamp"], y=per_timestamp['transaction_count'],
                    mode='lines+markers',
                    name=f"Orders per {time_interval}",
                    fill="tozeroy"
                    ),
        row=1, col=1
    )
    fig.add_trace(
        pgo.Bar(
            name="Bestellingen per product",
            x=per_product_blueprint["blueprint_name"],
            y=per_product_blueprint["transaction_count"],
            text=per_product_blueprint["transaction_count"],  # Display values
            textposition="auto"  # Automatically position the text
        ),
        row=1, col=2
    )

    st.plotly_chart(fig)
