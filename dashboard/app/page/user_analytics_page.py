import streamlit as st

from app.modules.core.core_api import fetch_user_table


def user_analytics():
    st.title("User Analytics")
    st.write(fetch_user_table())
