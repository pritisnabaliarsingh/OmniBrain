import faiss
import numpy as np
from fastapi import HTTPException
from app.utils.logger import logger

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

    if index is None or len(stored_chunks) == 0:
        logger.warning("FAISS Index is empty. Returning empty context.")
        return []

    distances, indices = index.search(
        np.array([query_embedding]).astype("float32"),
        top_k
    )

    results = []

    for idx in indices[0]:
        results.append(stored_chunks[idx])

    return results