from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Sample documents(to check)
SAMPLE_DOCS = [
    "Q3 revenue increased by 12% compared to the previous quarter, driven by strong product sales.",
    "The company's total assets grew to $450 million by the end of the fiscal year.",
    "Net profit margin improved from 8% to 11% due to cost optimization measures.",
    "The board approved a new investment strategy focusing on renewable energy projects.",
]

def build_retriever(documents=None, k=2):
    """
    Builds a FAISS-based retriever from a list of text documents.
    Uses a free, local embedding model (no API key required).
    """
    docs = documents if documents else SAMPLE_DOCS
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(docs, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": k})

if __name__ == "__main__":
    retriever = build_retriever()
    query = "What was the revenue growth?"
    results = retriever.invoke(query)

    print(f"Query: {query}\n")
    print("Top matching chunks:")
    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc.page_content}")
