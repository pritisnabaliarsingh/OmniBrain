import re
import fitz

def clean_text(raw_text: str) -> str:
     text = re.sub(r'(\w)-\n(\w)', r'\1\2', raw_text)  # fix hyphenated line breaks FIRST# collapse whitespace
     text = re.sub(r'\s+', ' ', text)                    # then collapse whitespace# fix hyphenated line breaks
     text = text.strip()
     return text

def extract_clean_pages(file_path: str) -> list:
    doc = fitz.open(file_path)
    pages = []
    for i, page in enumerate(doc):
        raw = page.get_text()
        pages.append({"page_number": i + 1, "text": clean_text(raw)})
    doc.close()
    return pages


if __name__ == "__main__":
    pages = extract_clean_pages("document_processing/samples/sample.pdf")
    for p in pages[:2]:
        print(p["page_number"], "->", p["text"][:200])
