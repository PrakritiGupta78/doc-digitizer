"""
FastAPI backend for AI-powered document digitization.

Run locally with:
    uvicorn main:app --reload

Then open http://127.0.0.1:8000/docs to test it interactively,
or open frontend/index.html in a browser to use the upload UI.
"""

import os
import shutil
import uuid

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ocr_engine import extract_text
from extractor import extract_fields

app = FastAPI(title="Document Digitization API")

# Allows the frontend (running from a different origin/file) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Document Digitization API is running"}


@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {sorted(ALLOWED_EXTENSIONS)}",
        )

    # Unique temp filename so concurrent uploads never collide
    temp_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}{ext}")

    try:
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        raw_text = extract_text(temp_path, engine="tesseract")
        fields = extract_fields(raw_text)

        return {
            "filename": file.filename,
            "raw_text": raw_text,
            "extracted_fields": fields,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
