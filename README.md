# AI-Powered Document Digitization (OCR)

Upload a photo or scan of a document (invoice, receipt, form) and get back
cleaned-up text plus automatically extracted fields (invoice number, date,
total, email, phone).

## Pipeline
1. **Preprocessing** (OpenCV) — deskew, denoise, adaptive threshold
2. **OCR** (Tesseract) — text extraction from the cleaned image
3. **Field extraction** (regex) — pulls structured fields from raw text
4. **API** (FastAPI) — `/extract` endpoint accepting an image upload
5. **Frontend** — plain HTML/JS upload UI

Prototyped and benchmarked in Google Colab (`/notebook`), then built into a
full application here.

## Run locally

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

You'll also need Tesseract installed system-wide:
- **Windows**: install from https://github.com/UB-Mannheim/tesseract/wiki, add it to PATH
- **Mac**: `brew install tesseract`
- **Linux**: `sudo apt install tesseract-ocr`

Then open `frontend/index.html` directly in a browser (or serve it) to use the upload UI.

## API

`POST /extract` — multipart form upload, field name `file`

```json
{
  "filename": "invoice.jpg",
  "raw_text": "...",
  "extracted_fields": {
    "invoice_number": "INV-2041",
    "date": "07/12/2026",
    "total": "1,240.00",
    "email": null,
    "phone": null
  }
}
```

## Deploy

Deployed via Docker on Render/Railway (Tesseract needs a system binary, so
a plain Python buildpack won't work — the included `Dockerfile` handles it).

## Tech stack

FastAPI · OpenCV · Tesseract OCR · Python · vanilla JS
