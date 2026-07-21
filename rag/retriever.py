from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

SAMPLE_DOCS = [
    "Q3 revenue increased by 12% compared to the previous quarter, driven by strong product sales.",
    "The company's total assets grew to $450 million by the end of the fiscal year.",
    "Net profit margin improved from 8% to 11% due to cost optimization measures.",
    "The board approved a new investment strategy focusing on renewable energy projects.",
]

def build_retriever(documents=None, k=2):
    docs = documents if documents else SAMPLE_DOCS
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(docs, embeddings)
    return vectorstore, vectorstore.as_retriever(search_kwargs={"k": k})


def retrieve_relevant_chunks(query, retriever):
    """Basic retrieval - just returns matching text."""
    if not query or query.strip() == "":
        return []
    results = retriever.invoke(query)
    return [doc.page_content for doc in results]


def retrieve_with_scores(query, vectorstore, k=2):
    """Retrieval with similarity scores - lower score = closer match in FAISS."""
    if not query or query.strip() == "":
        return []
    results = vectorstore.similarity_search_with_score(query, k=k)
    return [(doc.page_content, score) for doc, score in results]


if __name__ == "__main__":
    vectorstore, retriever = build_retriever()
    query = "What was the revenue growth?"

    print(f"Query: {query}\n")

    print("Basic retrieval:")
    for i, chunk in enumerate(retrieve_relevant_chunks(query, retriever), 1):
        print(f"{i}. {chunk}")

    print("\nWith similarity scores:")
    for i, (chunk, score) in enumerate(retrieve_with_scores(query, vectorstore, k=2), 1):
        print(f"{i}. (score: {score:.4f}) {chunk}")
