from app.utils.document_processing.extractors.ocr_extractor import extract_with_ocr_fallback
from app.utils.document_processing.extractors.table_extractor import extract_tables
from app.utils.document_processing.chunkers.tagged_chunker import tagged_chunks

def run_hybrid_pipeline(file_path: str) -> dict:
    text_pages = extract_with_ocr_fallback(file_path)   # handles native + scanned
    tables = extract_tables(file_path)
    chunks = tagged_chunks(text_pages)

    return {
        "chunks": chunks,
        "tables": tables,
        "total_chunks": len(chunks),
        "total_tables": len(tables)
    }


if __name__ == "__main__":
    result = run_hybrid_pipeline("document_processing/samples/sample.pdf")
    print(f"Chunks: {result['total_chunks']}, Tables: {result['total_tables']}")
