"""
Entry point for the Document Processing module.
Usage: python -m document_processing.main <path_to_pdf>
"""
import sys
from document_processing.integration.export_for_rag import export_for_rag
from document_processing.tests.qa_report import run_qa

def main(file_path: str):
    print("Running QA check...")
    qa = run_qa(file_path)
    print(qa)

    if qa["status"] == "REVIEW_NEEDED":
        print("WARNING: many blank pages detected - check if PDF is scanned/corrupted.")

    print("Exporting for RAG pipeline...")
    export_for_rag(file_path)
    print("Done.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m document_processing.main <path_to_pdf>")
        sys.exit(1)
    main(sys.argv[1])
