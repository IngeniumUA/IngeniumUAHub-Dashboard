import streamlit as st
from requests import post

from app.settings import settings

def authenticate_user_component():
    # Build login URL
    if "keycloak_token" in st.session_state:
        # TODO If timer expires this will bug
        return
    auth_url = f"{settings.keycloak_server_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/auth" \
               f"?client_id={settings.keycloak_client_id}&response_type=code&redirect_uri={"http://localhost:4200"}"
    st.markdown(f"[Click here to login]({auth_url})")

    # Exchange code for token
    if "code" in st.query_params:
        code = st.query_params["code"]
        token_url = f"{settings.keycloak_server_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/token"

        data = {
            "client_id": settings.keycloak_client_id,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://localhost:4200"
        }

        response = post(token_url, data=data)
        st.session_state.keycloak_token = response.json()
