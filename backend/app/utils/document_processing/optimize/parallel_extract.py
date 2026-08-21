import fitz
from concurrent.futures import ProcessPoolExecutor
from app.utils.document_processing.extractors.text_extractor import clean_text

def _process_single_page(args):
    file_path, page_num = args
    doc = fitz.open(file_path)
    text = clean_text(doc[page_num].get_text())
    doc.close()
    return {"page_number": page_num + 1, "text": text}

def parallel_extract(file_path: str, max_workers: int = 4) -> list:
    doc = fitz.open(file_path)
    n_pages = len(doc)
    doc.close()

    tasks = [(file_path, i) for i in range(n_pages)]
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(_process_single_page, tasks))
    return sorted(results, key=lambda x: x["page_number"])


if __name__ == "__main__":
    import time
    start = time.time()
    pages = parallel_extract("document_processing/samples/sample.pdf")
    print(f"Processed {len(pages)} pages in {time.time() - start:.2f}s")
