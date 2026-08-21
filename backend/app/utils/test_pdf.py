from pathlib import Path

from app.services.pdf_service import read_pdf
from app.services.chunk_service import split_text

SAMPLE_PDF = (
    Path(__file__).resolve().parent
    / "document_processing"
    / "samples"
    / "sample.pdf"
)

text = read_pdf(str(SAMPLE_PDF))

print("========== PDF TEXT ==========")
print(text)

chunks = split_text(text)

print("\nTotal Chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}")
    print(chunk)