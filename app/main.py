import streamlit as st
from core.config import APP_NAME
from app.auth.login import login

logged_in = login()

if not logged_in:
    st.stop()

st.success("Welcome! App shell is ready.")

st.set_page_config(
    page_title=APP_NAME,
    layout="wide",
)

st.title(APP_NAME)

st.info(
    """
    🚧 MVP under development.

    This is the bootstrap version of the Local AI-Enabled Data Cleaning Platform.
    """
)

st.write("If you see this page, Issue #1 is working ✅")