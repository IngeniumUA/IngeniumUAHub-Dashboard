import streamlit as st
from tornado.web import RequestHandler
from streamlit.web.server import Server

from app.page.lib.authentication import authenticate_user_component, is_authenticated, logout
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
from app.settings import settings, EnvironmentEnum


class SetTokenHandler(RequestHandler):
    def post(self):
        import json
        from datetime import datetime
        from app.page.cached_resources.keycloak_jwt import get_keycloak_jwt

        def save_received_token(token: dict) -> bool:
            if not all(k in token for k in ["expires_in", "access_token"]):
                st.session_state.keycloak_token = None
                st.session_state.keycloak_created = datetime.now()
                st.session_state.keycloak_user = None
                return False
            decoded = get_keycloak_jwt().validate_token(token["access_token"])
            st.session_state.keycloak_token = token
            st.session_state.keycloak_created = datetime.now()
            st.session_state.keycloak_user = decoded
            return True

        try:
            token_dict = json.loads(self.request.body)
            if save_received_token(token_dict):
                self.set_status(200)
                self.finish("OK")
            else:
                self.set_status(400)
                self.finish("Invalid token")
        except Exception as e:
            self.set_status(500)
            self.finish(str(e))

@st.cache_resource
def register_set_token_handler():
    server = Server.get_current()
    if server:
        app = server._http_app
        app.add_handlers(r".*", [(r"/set-token", SetTokenHandler)])

def run_main_app():
    # Top pages configuration
    st.set_page_config(layout="wide")

    # -----
    # Setup
    st.markdown("""
    <script>
    window.addEventListener("message", (event) => {
        if (event.origin !== "https://main.yourdomain.com") return; // SECURITY CHECK

        if (event.data.type === "auth") {
            fetch("/set-token", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(event.data.token)
            }).then(res => {
                if (res.ok) {
                    console.log("✅ Token stored in session_state");
                    // Optionally tell Python to re-run
                    window.parent.postMessage({ type: "token-set" }, event.origin);
                } else {
                    console.error("❌ Failed to set token");
                }
            }).catch(err => console.error(err));
        }
    });
    </script>
    """, unsafe_allow_html=True)

    authenticate_user_component()  # Authentication on user-level
    if not is_authenticated():
        st.warning("Not authenticated")
        if settings.running_environment.value != EnvironmentEnum.local.value:
            return
    else:
        col1, col2 = st.columns(2)
        col1.success("Authenticated")
        col2.button("Log out", on_click=logout)
    # st.write(st.session_state.get("keycloak_token", None))

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
