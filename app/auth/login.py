import streamlit as st

def login():
    st.subheader("Login (MVP)")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            st.success("Login successful (stub)")
            return True
        else:
            st.error("Enter credentials")

    return False