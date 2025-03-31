import streamlit as st

from app.modules.authentication.authentication import authenticate_user_component
from app.page.main_page import main_page
from app.page.transaction_analytics_page import transaction_analytics
from app.page.user_analytics_page import user_analytics


def run_main_app():
    # Top pages configuration
    pg = st.navigation(
        [
            st.Page(main_page),
            st.Page(user_analytics),
            st.Page(transaction_analytics),
        ]
    )
    pg.run()

    # General authentication code
    authenticate_user_component()


if __name__ == "__main__":
    run_main_app()
