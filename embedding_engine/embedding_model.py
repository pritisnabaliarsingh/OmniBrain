from langchain_community.embeddings import HuggingFaceEmbeddings
import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from document_processing.integration.export_for_rag import export_for_rag

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def get_real_sentences(pdf_path="document_processing/samples/sample.pdf"):
    records = export_for_rag(pdf_path)
    return [r["text"] for r in records]

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

if __name__ == "__main__":
    sentences = get_real_sentences()
    print(f"Loaded {len(sentences)} real document chunks.\n")

    vec1 = embeddings.embed_query(sentences[0])
    vec2 = embeddings.embed_query(sentences[1])

    similarity = cosine_similarity(vec1, vec2)
    print(f"Similarity between chunk 1 and chunk 2: {similarity:.4f}")
    print(f"\nEmbedding vector length: {len(vec1)} numbers")