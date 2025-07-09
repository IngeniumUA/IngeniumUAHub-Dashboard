from datetime import timedelta, datetime

import streamlit as st
from requests import post, Response

from app.page.cached_resources.keycloak_jwt import get_keycloak_jwt
from app.settings import settings

def is_valid_token(token: dict) -> bool:
    return all(key in token.keys() for key in ["expires_in", "access_token"])

def save_received_token(token: dict) -> bool:
    if not is_valid_token(token):
        st.session_state.keycloak_token = None
        st.session_state.keycloak_created = datetime.now()
        st.session_state.keycloak_user = None
        return False

    decoded = get_keycloak_jwt().validate_token(token.get("access_token"))

    st.session_state.keycloak_token = token
    st.session_state.keycloak_created = datetime.now()
    st.session_state.keycloak_user = decoded

    return True

def logout():
    st.session_state.keycloak_token = None
    st.session_state.keycloak_user = None
    st.session_state.keycloak_created = datetime.now()
    return

def is_authenticated() -> bool:
    if ("keycloak_token" not in st.session_state or
        "keycloak_created" not in st.session_state or
        "keycloak_user" not in st.session_state):
        return False

    token_dict: dict = st.session_state.keycloak_token
    token_created_timestamp = st.session_state.keycloak_created
    if token_dict is None:
        return False

    if not is_valid_token(token_dict):
        st.session_state.keycloak_token = None
        st.session_state.keycloak_created = datetime.now()
        return False

    if (datetime.now() - token_created_timestamp).seconds > token_dict.get("expires_in"):
        st.session_state.keycloak_token = None
        st.session_state.keycloak_created = datetime.now()
        return False

    sso_user = st.session_state.keycloak_user
    return "staff" in sso_user.get("realm_access", {}).get("roles", [])

@st.cache_resource(ttl=timedelta(seconds=1))
def authenticate_user_component():
    if is_authenticated():
        return

    # Build login URL
    auth_url = (
        f"{settings.keycloak_server_url}/realms/{settings.keycloak_realm}/protocol/openid-connect/auth"
        f"?client_id={settings.keycloak_frontend_client_id}&response_type=code"
        f"&redirect_uri={settings.redirect_uri_url}&scope=openid profile"
    )
    st.html(f"<a href='{auth_url}'>Click here to login</a>")

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
