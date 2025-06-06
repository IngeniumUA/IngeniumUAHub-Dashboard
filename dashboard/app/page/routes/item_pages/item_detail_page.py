import datetime

import streamlit as st
from streamlit.delta_generator import DeltaGenerator

import plotly.graph_objects as pgo

from app.page.cached_resources.clients import get_core_client

def item_line_chart(container: DeltaGenerator, key: str):
    """
    Same as bar chart but then grouped by datetime
    """
    fig = pgo.Figure()
    container.plotly_chart(figure_or_data=fig, use_container_width=True, key=f"{key}_line_chart")

def item_bar_chart(container: DeltaGenerator, key: str):
    """
    Same as line chart but then totals
    """
    fig = pgo.Figure()
    container.plotly_chart(figure_or_data=fig, use_container_width=True, key=f"{key}_bar_chart")


@st.fragment
def item_everything_graph_component(key: str, item_wide: dict):
    """
    @param key: Streamlit base key to be used (usually item identifier)
    @param item_wide: Dictionary of item being analysed in wide format
    --------------------------
    |  4/5          |  1/5   |
    |  time_grouped |  bar   |
    |  line chart   |  chart |
    --------------------------

    """
    # -----
    # Defining keys
    from_timestamp_key = f"{key}_from_timestamp"
    until_timestamp_key = f"{key}_until_timestamp"


    # ---
    # Pre-processing

    # ----
    # Display Step 1
    line_chart_container, bar_chart_container = st.columns(2)

    # As the configuration of both charts is done after they have rendered
    # We set defaults for the first render
    min_timestamp = datetime.datetime.strptime(item_wide["item"]["created_timestamp"], "%Y-%m-%dT%H:%M:%S.%f")
    max_timestamp = datetime.datetime.now(datetime.UTC)
    from_timestamp: datetime.datetime = st.session_state.get(from_timestamp_key,
                                                             min_timestamp)
    until_timestamp: datetime.datetime = st.session_state.get(until_timestamp_key,
                                                              max_timestamp)
    fields_to_group: list = []

    # Data collections
    transactions_df = ...
    checkouts_df = ...
    umami_df = ...

    # ----
    # Display Step 2
    item_line_chart(line_chart_container, key=key)
    item_bar_chart(bar_chart_container, key=key)

    # -----
    # Configuration
    st.subheader("Config")
    st.caption("Possible filter options will depend on selected timerange")

    date_col, time_col = st.columns(2)
    date_start = date_col.date_input("Select a start date", key="date_start",
                                     value=min_timestamp.date(),
                                     min_value=min_timestamp.date(), max_value=max_timestamp.date())
    time_start = time_col.time_input("Select a start time", key="time_start",
                                     value=min_timestamp.time())
    st.session_state.from_timestamp_key = datetime.datetime.combine(date_start, time_start)
    date_col, time_col = st.columns(2)
    date_end = date_col.date_input("Select an end date", key="date_end",
                                   value=max_timestamp.date(),
                                   min_value=min_timestamp.date(), max_value=max_timestamp.date())
    time_end = time_col.time_input("Select an end time", key="time_end", value=max_timestamp.time())
    st.session_state.until_timestamp_key = datetime.datetime.combine(date_end, time_end)


    with st.form(key="item_form", enter_to_submit=True, border=True):


        fields_to_group_options = []  # todo fetch from db
        st.multiselect(label="Fields to group", options=fields_to_group_options,
                       format_func=lambda v: v.replace("_", " ").title())

        update_filters = st.form_submit_button("Update")
    if update_filters:
        ...


def item_detail_page():
    # ----
    # Guard clauses with conditionals
    item_identifier: str = st.query_params.get("item", None)
    if not item_identifier:
        st.warning("Please provide item identifier")
        return

    core_client = get_core_client()
    item_detail = core_client.get_item_wide(item_identifier=item_identifier)
    if not item_detail:
        st.warning("Item could not be fetched")
        return

    # -----
    # Pre processing

    # -----
    # Display
    st.title(item_detail["item"]["name"])
    st.caption(item_detail["derived_type"]["derived_type_enum"].replace("_", " ").title())

    item_everything_graph_component(item_wide=item_detail, key=item_detail["item"]["id"])
