import streamlit as st

from app.page.lib.authentication import authenticate_user_component
from app.page.routes.cloud_analytics_page import cloud_detail_page
from app.page.routes.duck_ingestion_page import duck_ingestion_page
from app.page.routes.item_pages.item_detail_page import item_detail_page
from app.page.routes.item_pages.items_overview_page import items_overview_page
from app.page.routes.main_page import main_page
from app.page.routes.ordertracking_analytics_page import order_tracking_analytics_page
from app.page.routes.transaction_analytics_page import transaction_analytics_page
from app.page.routes.user_analytics_page import user_analytics


def run_main_app():
    # Top pages configuration
    st.set_page_config(layout="wide")

    # -----
    # Setup
    authenticate_user_component()  # Authentication on user-level
    if "keycloak_token" not in st.session_state:
        st.warning("Not authenticated")
        # return

    # -----
    # Pages
    pg = st.navigation(
        [
            st.Page(main_page),
            st.Page(duck_ingestion_page),
            st.Page(user_analytics),
            st.Page(transaction_analytics_page),
            st.Page(order_tracking_analytics_page),
            st.Page(items_overview_page),
            st.Page(page=item_detail_page, title="Item Detail"),
            st.Page(page=cloud_detail_page, title="Cloud Analytics"),
        ]
    )
    pg.run()


if __name__ == "__main__":
    run_main_app()
