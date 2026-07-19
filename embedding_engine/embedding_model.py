from langchain_community.embeddings import HuggingFaceEmbeddings
import numpy as np

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

sentence1 = "Revenue grew by 12% this quarter."
sentence2 = "Sales increased significantly in Q3."
sentence3 = "The weather was sunny yesterday."

vec1 = embeddings.embed_query(sentence1)
vec2 = embeddings.embed_query(sentence2)
vec3 = embeddings.embed_query(sentence3)

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(f"Similarity (revenue vs sales): {cosine_similarity(vec1, vec2):.4f}")
print(f"Similarity (revenue vs weather): {cosine_similarity(vec1, vec3):.4f}")
print(f"\nEmbedding vector length: {len(vec1)} numbers")
print(f"First 5 numbers of sentence 1's embedding: {vec1[:5]}")