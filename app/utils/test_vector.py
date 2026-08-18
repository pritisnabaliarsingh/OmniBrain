from app.services.pdf_service import read_pdf
from app.services.chunk_service import split_text
from app.services.embedding_service import create_embeddings
from app.services.vector_store import create_vector_store

# Read PDF
text = read_pdf("uploads/sample.pdf")

# Split into chunks
chunks = split_text(text)

# Create embeddings
embeddings = create_embeddings(chunks)

# Create FAISS vector store
create_vector_store(embeddings, chunks)

print("Vector Store Created Successfully!")
print("Total Chunks:", len(chunks))
print("Embedding Shape:", embeddings.shape)