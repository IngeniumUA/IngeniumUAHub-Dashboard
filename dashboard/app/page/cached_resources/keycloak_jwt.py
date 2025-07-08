import streamlit as st

from app.modules.keycloak.keycloak_jwt import KeycloakJWT
from app.settings import settings


@st.cache_resource
def get_keycloak_jwt():
    return KeycloakJWT(settings.keycloak_jwks_uri)
