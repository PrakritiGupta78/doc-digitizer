"""
Structured field extraction from raw OCR text.
Same regex patterns tested in the Colab notebook.
"""

import re

FIELD_PATTERNS = {
    "invoice_number": r"(?:invoice|inv)\s*#?\s*[:\-]?\s*([A-Z0-9\-]{4,})",
    "date": r"(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
    "total": r"\b(?:grand total|amount due|total)\b\s*[:\-]?\s*\$?\s*([\d,]+\.\d{2})",
    "email": r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
    "phone": r"(\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4})",
}

# Fallback for when OCR drops the "Total:" label entirely (common with
# multi-column layouts where label and value sit far apart on the page).
# In that case, fall back to the last dollar-sign-prefixed amount in the
# document -- totals are conventionally the one number marked with "$",
# while line items and subtotals are often left unmarked.
DOLLAR_AMOUNT_PATTERN = r"\$\s*([\d,]+\.\d{2})"


def extract_fields(text: str) -> dict:
    fields = {}
    for field_name, pattern in FIELD_PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)
        fields[field_name] = match.group(1) if match else None

    if fields.get("total") is None:
        dollar_matches = re.findall(DOLLAR_AMOUNT_PATTERN, text)
        if dollar_matches:
            fields["total"] = dollar_matches[-1]  # last $ amount = most likely the total

    return fields