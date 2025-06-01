import streamlit as st

from app.page.routes.duck_ingestion_page import duck_ingestion_page
from app.page.routes.main_page import main_page
from app.page.routes.ordertracking_analytics_page import order_tracking_analytics_page
from app.page.routes.transaction_analytics_page import transaction_analytics_page
from app.page.routes.user_analytics_page import user_analytics


def run_main_app():
    # Top pages configuration
    st.set_page_config(layout="wide")

    # -----
    # Setup

    # -----
    # Pages
    pg = st.navigation(
        [
            st.Page(main_page),
            st.Page(duck_ingestion_page),
            st.Page(user_analytics),
            st.Page(transaction_analytics_page),
            st.Page(order_tracking_analytics_page),
        ]
    )
    pg.run()


if __name__ == "__main__":
    run_main_app()
