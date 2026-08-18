from app.services.pdf_service import read_pdf
from app.services.chunk_service import split_text
from app.services.embedding_service import create_embeddings

text = read_pdf("uploads/sample.pdf")

chunks = split_text(text)

embeddings = create_embeddings(chunks)

print("Number of Chunks:", len(chunks))
print("Embedding Shape:", embeddings.shape)