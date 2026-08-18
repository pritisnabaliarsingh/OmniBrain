import fitz
import pytesseract
from PIL import Image
import io

def is_scanned_page(page, text_threshold: int = 20) -> bool:
    """Heuristic: if extractable text is too short, page is likely scanned."""
    return len(page.get_text().strip()) < text_threshold

def ocr_page(page, zoom: int = 2) -> str:
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    return pytesseract.image_to_string(img)

def extract_with_ocr_fallback(file_path: str) -> list:
    doc = fitz.open(file_path)
    results = []
    for i, page in enumerate(doc):
        if is_scanned_page(page):
            text = ocr_page(page)
            method = "ocr"
        else:
            text = page.get_text()
            method = "native"
        results.append({"page_number": i + 1, "text": text, "method": method})
    doc.close()
    return results


if __name__ == "__main__":
    pages = extract_with_ocr_fallback("document_processing/samples/sample.pdf")
    for p in pages[:2]:
        print(p["page_number"], p["method"], "->", p["text"][:150])
