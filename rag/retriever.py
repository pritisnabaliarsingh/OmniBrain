from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

SAMPLE_DOCS = [
    "Q3 revenue increased by 12% compared to the previous quarter, driven by strong product sales.",
    "The company's total assets grew to $450 million by the end of the fiscal year.",
    "Net profit margin improved from 8% to 11% due to cost optimization measures.",
    "The board approved a new investment strategy focusing on renewable energy projects.",
]

_vectorstore_cache = None

def get_vectorstore(documents=None):
    global _vectorstore_cache
    if _vectorstore_cache is None:
        docs = documents if documents else SAMPLE_DOCS
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        _vectorstore_cache = FAISS.from_texts(docs, embeddings)
    return _vectorstore_cache

def get_retriever(search_type="similarity", k=2, documents=None):
    vectorstore = get_vectorstore(documents)
    return vectorstore.as_retriever(search_type=search_type, search_kwargs={"k": k})

if __name__ == "__main__":
    query = "What was the revenue growth?"
    print("=== Similarity search ===")
    retriever = get_retriever(search_type="similarity", k=2)
    for i, doc in enumerate(retriever.invoke(query), 1):
        print(f"{i}. {doc.page_content}")
    print("\n=== MMR search (more diverse results) ===")
    retriever_mmr = get_retriever(search_type="mmr", k=2)
    for i, doc in enumerate(retriever_mmr.invoke(query), 1):
        print(f"{i}. {doc.page_content}")