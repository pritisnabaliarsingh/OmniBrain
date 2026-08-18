import os

def validate_pdf_path(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    if not file_path.lower().endswith(".pdf"):
        raise ValueError(f"Not a PDF file: {file_path}")

def safe_extract(func, *args, **kwargs):
    """Wrap any extractor call so one bad page doesn't crash the whole pipeline."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"[WARN] {func.__name__} failed: {e}")
        return None
