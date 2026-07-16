FROM python:3.11-slim

# Tesseract is a system binary, not a pip package — must be installed via apt
RUN apt-get update && \
    apt-get install -y tesseract-ocr libgl1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY backend/ .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
