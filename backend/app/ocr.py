# app/ocr.py
from PIL import Image
import pytesseract
from typing import List

# Remove or comment out any old tesseract_cmd line
# pytesseract.pytesseract.tesseract_cmd = r"..."

def extract_text(image_path: str) -> str:
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang="eng")
    return text


def infer_fields_from_text(text: str) -> List[str]:
    # For v1: hard-code or very naive extraction
    # Example hard-coded fields for a simple KYC-like form
    return [
        "Full Name",
        "Date of Birth",
        "Address",
        "Mobile Number",
        "Email"
    ]
