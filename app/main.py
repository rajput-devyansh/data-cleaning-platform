import streamlit as st
from app.auth.login import login

st.set_page_config(layout="wide")

if not login():
    st.stop()

st.sidebar.title("Pipeline Steps")

page = st.sidebar.radio(
    "Navigate",
    ["Ingestion", "Schema"],
)

if page == "Ingestion":
    import app.pages.ingestion
elif page == "Schema":
    import app.pages.schema