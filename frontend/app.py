import streamlit as st
import requests

st.set_page_config(page_title="SmartSupport AI")
st.title("🤖 SmartSupport AI")

BACKEND_URL = "http://127.0.0.1:8000/chat"

user_input = st.text_input("Ask something:")

if st.button("Send") and user_input:
    payload = {"message": user_input}

    try:
        res = requests.post(BACKEND_URL, json=payload)
        data = res.json()
        st.success(data["reply"])
    except Exception as e:
        st.error(f"Error: {e}")
