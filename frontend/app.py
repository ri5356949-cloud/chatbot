import streamlit as st
import requests

st.title("📄 Smart Support AI")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    files = {"file": uploaded_file}
    requests.post("http://127.0.0.1:8000/upload-pdf", files=files)
    st.success("PDF uploaded")

question = st.text_input("Ask your question")

if st.button("Ask"):
    res = requests.post(
        "http://127.0.0.1:8000/ask",
        json={"question": question}
    )
    data = res.json()

    st.write("### Answer:")
    st.write(data["answer"])
    st.caption(f"Source: {data['source']}")
