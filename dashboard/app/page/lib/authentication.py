from datetime import timedelta, datetime

import streamlit as st
from requests import post, Response

from app.settings import settings

def save_received_token(token: dict) -> bool:
    st.session_state.keycloak_token = token
    st.session_state.keycloak_created = datetime.now()
    return True

def is_authenticated() -> bool:
    if "keycloak_token" not in st.session_state or "keycloak_created" not in st.session_state:
        return False

    token_dict: dict = st.session_state.keycloak_token
    token_created_timestamp = st.session_state.keycloak_created
    if not all(key in token_dict.keys() for key in ["expires_in", "access_token"]):
        st.session_state.keycloak_token = None
        st.session_state.keycloak_created = datetime.now()
        return False

    if (datetime.now() - token_created_timestamp).seconds > token_dict.get("expires_in"):
        st.session_state.keycloak_token = None
        st.session_state.keycloak_created = datetime.now()
        return False

    return True

@st.cache_resource(ttl=timedelta(seconds=1))
def authenticate_user_component():
    if is_authenticated():
        return

    # Build login URL
    auth_url = (
        f"{settings.keycloak_server_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/auth"
        f"?client_id={settings.keycloak_frontend_client_id}&response_type=code&redirect_uri={'http://localhost:4200'}"
    )
    st.markdown(f"[Click here to login]({auth_url})")

    # Exchange code for token
    if "code" in st.query_params:
        code = st.query_params["code"]
        token_url = f"{settings.keycloak_server_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/token"

        data = {
            "client_id": settings.keycloak_frontend_client_id,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://localhost:4200",
        }

        response: Response = post(token_url, data=data)
        save_received_token(response.json()) # Parsed as dict!
