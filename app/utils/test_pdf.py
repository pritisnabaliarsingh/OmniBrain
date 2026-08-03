from app.services.pdf_service import read_pdf
from app.services.chunk_service import split_text

text = read_pdf("uploads/sample.pdf")

print("========== PDF TEXT ==========")
print(text)

chunks = split_text(text)

print("\nTotal Chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i+1}")
    print(chunk)