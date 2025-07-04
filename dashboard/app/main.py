import streamlit as st

from app.page.lib.authentication import authenticate_user_component
from app.page.routes.cloud_analytics_page import cloud_detail_page
from app.page.routes.data_sync_status_page import data_sync_status_page
from app.page.routes.dblog_page import dblog_page
from app.page.routes.item_pages.item_detail_page import item_detail_page
from app.page.routes.item_pages.items_overview_page import items_overview_page
from app.page.routes.main_page import main_page
from app.page.routes.ordertracking_analytics_page import order_tracking_analytics_page
from app.page.routes.popupz.popupz_products_report import popupz_orders_report_page
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
    else:
        st.success("Authenticated")

    # -----
    # Pages
    pg = st.navigation({
            "Data application": [st.Page(page=main_page, title="Main"),
                                 st.Page(page=data_sync_status_page, title="Data sync")],
            "Dashboards": [
                st.Page(page=cloud_detail_page, title="Cloud Analytics"),
                st.Page(page=user_analytics, title="User analytics"),
                st.Page(page=transaction_analytics_page, title="Transaction analytics"),
                st.Page(page=order_tracking_analytics_page, title="Order Tracking analytics"),
                st.Page(page=items_overview_page, title="Items Overview page"),
                st.Page(page=dblog_page, title="DBLog Overview page"),
            ],
            "Pop-up Z": [],
            "One-off reports": [st.Page(page=popupz_orders_report_page, title="Popup Z Orders Report")],
            "Embed pages": [st.Page(page=item_detail_page, title="Item Detail")]
        }
    )
    pg.run()


if __name__ == "__main__":
    run_main_app()
