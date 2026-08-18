import faiss
import numpy as np
from fastapi import HTTPException

index = None
stored_chunks = []


def create_vector_store(embeddings, chunks):
    global index, stored_chunks

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings).astype("float32"))

    stored_chunks = chunks

    print("Vector Store Created Successfully")

    return index


def search(query_embedding, top_k=3):
    global index, stored_chunks

    if index is None:
        raise HTTPException(
            status_code=400,
            detail="No PDF uploaded. Please upload a PDF first."
        )

    distances, indices = index.search(
        np.array([query_embedding]).astype("float32"),
        top_k
    )

    results = []

    for idx in indices[0]:
        results.append(stored_chunks[idx])

    return results