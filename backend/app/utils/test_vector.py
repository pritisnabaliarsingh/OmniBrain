from pathlib import Path

from app.services.pdf_service import read_pdf
from app.services.chunk_service import split_text
from app.services.embedding_service import create_embeddings
from app.services.vector_store import create_vector_store

SAMPLE_PDF = (
    Path(__file__).resolve().parent
    / "document_processing"
    / "samples"
    / "sample.pdf"
)

text = read_pdf(str(SAMPLE_PDF))

chunks = split_text(text)

embeddings = create_embeddings(chunks)

create_vector_store(embeddings, chunks)

print("Vector Store Created Successfully!")
print("Total Chunks:", len(chunks))
print("Embedding Shape:", embeddings.shape)