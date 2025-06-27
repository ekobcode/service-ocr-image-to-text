import pytesseract
from PIL import Image
from io import BytesIO
import requests
import re

def clean_ocr_text(text: str) -> str:
    """Clean OCR output for readability."""
    text = re.sub(r'-\n', '', text)             # Fix line-break hyphenation
    text = re.sub(r'\n+', ' ', text)            # Replace multiple newlines with space
    text = re.sub(r'\s{2,}', ' ', text)         # Collapse multiple spaces
    return text.strip()

def ocr_from_url(image_url: str, lang="eng", output="clean") -> dict:
    """Perform OCR on an image from a URL."""
    try:
        response = requests.get(image_url)
        content_type = response.headers.get("Content-Type", "")

        if not response.ok or "image" not in content_type:
            return {
                "status": "error",
                "message": "The provided URL is not a valid image.",
                "text": ""
            }

        image = Image.open(BytesIO(response.content))
        raw_text = pytesseract.image_to_string(image, lang=lang)
        text = raw_text if output == "raw" else clean_ocr_text(raw_text)

        return {
            "status": "success",
            "message": "Text extracted from image URL.",
            "text": text
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to process image from URL: {str(e)}",
            "text": ""
        }

def ocr_from_file(file_bytes: bytes, lang="eng", output="clean") -> dict:
    """Perform OCR on an uploaded image file."""
    try:
        image = Image.open(BytesIO(file_bytes))
        raw_text = pytesseract.image_to_string(image, lang=lang)
        text = raw_text if output == "raw" else clean_ocr_text(raw_text)

        return {
            "status": "success",
            "message": "Text extracted from uploaded image file.",
            "text": text
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to process uploaded file: {str(e)}",
            "text": ""
        }
