import streamlit as st
import fitz  
import vertexai
from vertexai.generative_models import GenerativeModel
import tempfile
import os


vertexai.init(project="legall-472707", location="us-central1")
model = GenerativeModel("gemini-2.5-pro")


def extract_text_from_pdf(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_file.read())
        tmp_path = tmp.name
    doc = fitz.open(tmp_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    os.remove(tmp_path)
    return text.strip()



st.set_page_config(page_title="DocuGuard AI", layout="wide")
st.title("📑 DocuGuard AI")
st.markdown("Your AI-powered assistant for **Simplification, Risk Analysis, Compliance, and Q&A**")


if "messages" not in st.session_state:
    st.session_state.messages = []


uploaded_file = st.file_uploader("📂 Upload a Legal PDF", type=["pdf"])

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)

   
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✨ Simplify"):
            prompt = f"""
            Summarize this legal text into clear bullet points in plain English.
            Focus on obligations and responsibilities.

            --- Document ---
            {text}
            """
            resp = model.generate_content(prompt)
            st.session_state.messages.append(("Simplified", resp.text))

    with col2:
        if st.button("⚠️ Risk Analyzer"):
            prompt = f"""
            Analyze the following legal text and list the key risks and penalties.
            Answer in bullet points, plain English.

            --- Document ---
            {text}
            """
            resp = model.generate_content(prompt)
            st.session_state.messages.append(("Risks", resp.text))

    with col3:
        if st.button("✅ Compliance Checker"):
            prompt = f"""
            Check the following legal text for compliance issues.
            Highlight obligations, financial penalties, and critical terms in bullet points.

            --- Document ---
            {text}
            """
            resp = model.generate_content(prompt)
            st.session_state.messages.append(("Compliance", resp.text))


question = st.text_input("💬 Ask a Question about Legal Docs")
if st.button("Send"):
    if question.strip():
        prompt = f"""
        You are a legal assistant. Answer the following question in **bullet points, plain English**:

        {question}
        """
        resp = model.generate_content(prompt)
        st.session_state.messages.append(("Answer", resp.text))


if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []


st.subheader("📌 Results")
for label, msg in st.session_state.messages:
    st.markdown(f"**{label}:**")
    st.markdown(msg)
    st.markdown("---")


