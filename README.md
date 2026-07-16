🔗 **Live demo:** https://doc-digitizer-iuwv.onrender.com
(Free-tier hosting — if it's been idle, the first request may take 30–60 seconds to wake up.)
# 📄 Document Digitizer

**Turn a photo of an invoice into structured data — automatically.**

Upload a scanned or photographed document, and this app cleans up the image,
reads the text with OCR, and pulls out the fields that actually matter
(invoice number, date, total, email, phone) — no manual typing required.

🔗 **Live demo:** https://doc-digitizer-iuwv.onrender.com
> Hosted on Render's free tier — if it's been idle, the first request may take 30–60 seconds to wake up.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?logo=opencv&logoColor=white)
![Tesseract](https://img.shields.io/badge/OCR-Tesseract-4285F4)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## Why this exists

Manually re-typing data from scanned invoices and receipts is slow and
error-prone. This project automates it: point a camera or scanner at a
document, and get clean, structured output back in seconds.

## How it works

```
 📷 Upload          🧹 Preprocess           👁️ OCR              🎯 Extract
 image      ───▶    deskew, denoise,  ───▶  read the      ───▶  pull out invoice #,
                     adaptive threshold      text (Tesseract)     date, total, email, phone
```

1. **Preprocessing (OpenCV)** — straightens tilted photos, removes noise,
   and applies adaptive thresholding so text stands out cleanly regardless
   of lighting conditions.
2. **OCR (Tesseract)** — a deep-learning-based OCR engine reads the cleaned
   image and returns raw text.
3. **Field extraction (regex, with fallback logic)** — parses the raw text
   for known patterns. If a labeled field can't be found (a real issue
   uncovered during testing on multi-column layouts — see
   [`PROJECT_DOCUMENTATION.md`](./PROJECT_DOCUMENTATION.md)), it falls back
   to a more general pattern instead of failing silently.
4. **FastAPI backend** serves both the API and the upload page from a single
   deployed URL.

## ✨ Features

- Drag-and-drop upload UI, no separate frontend hosting needed
- Automatic image cleanup before OCR (deskew, denoise, adaptive threshold)
- Structured field extraction: invoice number, date, total, email, phone
- Fallback extraction logic for messy/unlabeled OCR output
- Fully containerized with Docker — runs identically locally and in production
- Interactive API docs out of the box (`/docs`)

## 🧠 Benchmarked, not guessed

Two OCR engines (Tesseract and EasyOCR) were prototyped and compared side by
side in Google Colab before building the app — see
[`notebook/Document_Digitization_OCR.ipynb`](./notebook) for the full
preprocessing pipeline, benchmark, and word-error-rate evaluation that
informed the final engine choice.

## 🛠️ Tech Stack

| Layer | Tool | Why |
|---|---|---|
| Prototyping | Google Colab | Fast iteration, no local setup |
| Image preprocessing | OpenCV | Industry-standard computer vision |
| OCR | Tesseract (LSTM-based) | Free, local, no API cost, reliable on printed text |
| Field extraction | Python regex | Fast, no training data needed for structured formats |
| Backend | FastAPI + Uvicorn | Fast, async, automatic interactive docs |
| Frontend | Vanilla HTML/CSS/JS | Simple, dependency-free, served directly by the backend |
| Deployment | Docker → Render | Tesseract needs a system binary — Docker keeps dev/prod identical |

## 🚀 Run it locally

```bash
git clone https://github.com/PrakritiGupta78/doc-digitizer.git
cd doc-digitizer/backend

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
uvicorn main:app --reload
```

Then open **http://127.0.0.1:8000** — the upload page and API are served
from the same address.

**Requires Tesseract installed system-wide:**
- Windows: [UB-Mannheim installer](https://github.com/UB-Mannheim/tesseract/wiki)
- Mac: `brew install tesseract`
- Linux: `sudo apt install tesseract-ocr`

## 📁 Project structure

```
doc-digitizer/
├── backend/
│   ├── main.py           # FastAPI app — API routes + serves the frontend
│   ├── ocr_engine.py     # Image preprocessing + OCR
│   ├── extractor.py      # Regex-based structured field extraction
│   ├── static/
│   │   └── index.html    # Upload UI
│   └── requirements.txt
├── notebook/
│   └── Document_Digitization_OCR.ipynb   # Colab prototyping + benchmark
├── Dockerfile
├── PROJECT_DOCUMENTATION.md   # Full architecture write-up
└── README.md
```

## 📡 API

**`POST /extract`** — multipart upload, field name `file`

```json
{
  "filename": "invoice.jpg",
  "raw_text": "...",
  "extracted_fields": {
    "invoice_number": "INV-20458",
    "date": "07/16/2026",
    "total": "1,240.00",
    "email": "rohan.sharma@example.com",
    "phone": "987-654-3210"
  }
}
```

Full interactive docs available at `/docs` on any running instance.

## ⚠️ Known limitations

- **Handwriting isn't reliably supported** — Tesseract is trained on printed
  fonts, not handwriting.
- **Unusual multi-column layouts can trip up OCR** — this is why extraction
  includes fallback logic rather than relying solely on labeled patterns.
- **Regex-based extraction assumes a reasonably standard invoice/receipt
  format** — a trained NER model would generalize better to wildly different
  layouts (see Roadmap).

## 🗺️ Roadmap

- [ ] CNN-based handwritten digit recognition (MNIST-trained) for handwritten fields
- [ ] Swap in EasyOCR or a cloud OCR API as a fallback engine for low-confidence pages
- [ ] Confidence scores per extracted field
- [ ] Replace regex extraction with a trained NER model for layout flexibility

## 📄 License

MIT — see [`LICENSE`](./LICENSE).
