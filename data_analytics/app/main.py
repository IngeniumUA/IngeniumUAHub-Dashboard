import streamlit as st

from app.page.main_page import main_page
from app.page.user_analytics_page import user_analytics


def run_main_app():
    pg = st.navigation([
        st.Page(main_page),
        st.Page(user_analytics),
    ])
    pg.run()

if __name__ == "__main__":
    run_main_app()
