from document_processing.extractors.text_extractor import extract_clean_pages
from document_processing.extractors.table_extractor import extract_tables
from document_processing.extractors.image_extractor import extract_images
from document_processing.extractors.metadata_extractor import extract_metadata

def run_qa(file_path: str) -> dict:
    text_pages = extract_clean_pages(file_path)
    tables = extract_tables(file_path)
    images = extract_images(file_path)
    meta = extract_metadata(file_path)

    empty_pages = [p["page_number"] for p in text_pages if len(p["text"]) < 10]

    report = {
        "total_pages": meta["page_count"],
        "pages_with_no_text": empty_pages,
        "tables_found": len(tables),
        "images_found": len(images),
        "status": "OK" if len(empty_pages) < meta["page_count"] * 0.3 else "REVIEW_NEEDED"
    }
    return report


if __name__ == "__main__":
    report = run_qa("document_processing/samples/sample.pdf")
    print(report)
