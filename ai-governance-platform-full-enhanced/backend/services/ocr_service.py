from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import tempfile
import magic

def extract_text_from_image(image_path: str) -> str:
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        return ""

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        texts = []
        images = convert_from_path(pdf_path, dpi=200)
        for img in images:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                img.save(tmp.name, "PNG")
                texts.append(pytesseract.image_to_string(Image.open(tmp.name)))
        return "\n".join(texts)
    except Exception as e:
        return ""

def extract_text_from_file(file_path: str) -> str:
    try:
        m = magic.from_file(file_path, mime=True)
    except Exception:
        m = None
    if m and "pdf" in m:
        return extract_text_from_pdf(file_path)
    else:
        return extract_text_from_image(file_path)
