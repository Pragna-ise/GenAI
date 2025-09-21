import streamlit as st
import fitz  # PyMuPDF
import vertexai
from vertexai.generative_models import GenerativeModel
import tempfile
import os

# Initialize Gemini
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

st.title("📑 DocuGuard AI – Legal Document Simplifier")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    st.subheader("Original Extracted Text")
    st.write(text[:1000] + "..." if len(text) > 1000 else text)

    if st.button("Simplify Document"):
        prompt = f"Summarize the following legal text into bullet points with key obligations and risks:\n\n{text}"
        resp = model.generate_content(prompt)
        st.subheader("Simplified Output")
        st.write(resp.text)

question = st.text_input("Ask a question about legal documents:")
if st.button("Ask"):
    prompt = f"Answer the following question in bullet points:\n\n{question}"
    resp = model.generate_content(prompt)
    st.subheader("Answer")
    st.write(resp.text)
