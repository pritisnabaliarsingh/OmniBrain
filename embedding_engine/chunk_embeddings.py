from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

SAMPLE_DOCS = [
    "Q3 revenue increased by 12% compared to the previous quarter, driven by strong product sales.",
    "The company's total assets grew to $450 million by the end of the fiscal year.",
    "Net profit margin improved from 8% to 11% due to cost optimization measures.",
    "The board approved a new investment strategy focusing on renewable energy projects.",
]

def search_with_threshold(query, documents=None, threshold=0.3, max_results=3):
    """
    Searches documents and only returns results above a similarity threshold.
    Prevents forcing irrelevant results just to fill a fixed count.
    """
    docs = documents if documents else SAMPLE_DOCS
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(docs, embeddings)

    # similarity_search_with_score returns (document, distance) — lower distance = more similar
    results = vectorstore.similarity_search_with_score(query, k=max_results)

    filtered = []
    for doc, score in results:
        # FAISS returns distance (lower = better), convert to a similarity-style number
        similarity = 1 / (1 + score)
        if similarity >= threshold:
            filtered.append((doc.page_content, round(similarity, 4)))

    return filtered

if __name__ == "__main__":
    query = "What was the revenue growth?"
    results = search_with_threshold(query, threshold=0.3)

    print(f"Query: {query}\n")
    if results:
        print("Relevant results (above threshold):")
        for text, score in results:
            print(f"- ({score}) {text}")
    else:
        print("No sufficiently relevant results found.")