"""
OCR engine module.
This is the same preprocessing + OCR logic prototyped in the Colab notebook,
moved here so the FastAPI app can call it directly.
"""
import cv2
import numpy as np
import pytesseract
import time
import os
import platform
if platform.system() == "Windows":
    windows_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(windows_path):
        pytesseract.pytesseract.tesseract_cmd = windows_path


def deskew(img):
    """Detects and corrects rotation/skew in a scanned document."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    if len(coords) < 10:
        return img  # not enough signal to estimate angle safely

    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )
    return rotated


def preprocess_image(path):
    """Full preprocessing pipeline: deskew -> grayscale -> denoise -> adaptive threshold."""
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"Could not read image: {path}")

    deskewed = deskew(img)
    gray = cv2.cvtColor(deskewed, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=30)
    thresh = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2
    )
    return thresh


def run_tesseract(path):
    """Preprocess + run Tesseract OCR. Returns (text, seconds_elapsed)."""
    processed = preprocess_image(path)
    start = time.time()
    text = pytesseract.image_to_string(processed)
    elapsed = time.time() - start
    return text.strip(), elapsed


def extract_text(path, engine: str = "tesseract"):
    """Public entry point used by the API layer."""
    if engine == "tesseract":
        text, _ = run_tesseract(path)
        return text
    raise ValueError(f"Unsupported engine: {engine}")
