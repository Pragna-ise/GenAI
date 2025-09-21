from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import fitz  
import vertexai
from vertexai.generative_models import GenerativeModel
import os, tempfile, traceback


app = FastAPI(title="DocuGuard AI")


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


vertexai.init(project="legall-472707", location="us-central1")
model = GenerativeModel("gemini-2.5-pro")


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text.strip()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return JSONResponse({"message": f"Uploaded {file.filename}"})


@app.post("/simplify")
async def simplify_doc(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        text = extract_text_from_pdf(tmp_path)
        os.remove(tmp_path)

        prompt = f"""
        Simplify this legal document into clear bullet points. 
        Focus on obligations, responsibilities, and rights.

        --- Document ---
        {text}
        """
        resp = model.generate_content(prompt)

        return JSONResponse({"simplified": resp.text.strip()})
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/risk")
async def analyze_risk(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        text = extract_text_from_pdf(tmp_path)
        os.remove(tmp_path)

        prompt = f"""
        Analyze risks in this legal document. 
        Highlight penalties, liabilities, hidden fees, and termination risks.
        Provide bullet points.

        --- Document ---
        {text}
        """
        resp = model.generate_content(prompt)

        return JSONResponse({"risks": resp.text.strip()})
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/compliance")
async def compliance_check(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        text = extract_text_from_pdf(tmp_path)
        os.remove(tmp_path)

        prompt = f"""
        Check compliance issues in this legal document. 
        Point out possible violations of common corporate, financial, or regulatory standards.
        Provide bullet points.

        --- Document ---
        {text}
        """
        resp = model.generate_content(prompt)

        return JSONResponse({"compliance": resp.text.strip()})
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/ask")
async def ask_question(question: str = Form(...)):
    try:
        prompt = f"""
        Answer the following question about legal documents in plain English bullet points:

        {question}
        """
        resp = model.generate_content(prompt)

        return JSONResponse({"answer": resp.text.strip()})
    except Exception as e:
        traceback.print_exc()
        return JSONResponse({"error": str(e)}, status_code=500)


