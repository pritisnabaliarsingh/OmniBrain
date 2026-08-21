from pathlib import Path

from app.services.pdf_service import read_pdf
from app.services.chunk_service import split_text
from app.services.embedding_service import create_embeddings

SAMPLE_PDF = (
    Path(__file__).resolve().parent
    / "document_processing"
    / "samples"
    / "sample.pdf"
)

text = read_pdf(str(SAMPLE_PDF))

chunks = split_text(text)

embeddings = create_embeddings(chunks)

print("Number of Chunks:", len(chunks))
print("Embedding Shape:", embeddings.shape)