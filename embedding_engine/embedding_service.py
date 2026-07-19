from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

SAMPLE_DOCS = [
    "Q3 revenue increased by 12% compared to the previous quarter, driven by strong product sales.",
    "The company's total assets grew to $450 million by the end of the fiscal year.",
    "Net profit margin improved from 8% to 11% due to cost optimization measures.",
    "The board approved a new investment strategy focusing on renewable energy projects.",
]

DB_PATH = "faiss_index"

def build_and_save_vector_db(documents=None):
    """Creates a FAISS vector database and saves it to disk."""
    docs = documents if documents else SAMPLE_DOCS
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(docs, embeddings)
    vectorstore.save_local(DB_PATH)
    print(f"Vector database saved to '{DB_PATH}/'")
    return vectorstore

def load_vector_db():
    """Loads an existing FAISS vector database from disk."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
    print(f"Vector database loaded from '{DB_PATH}/'")
    return vectorstore

if __name__ == "__main__":
    if os.path.exists(DB_PATH):
        vectorstore = load_vector_db()
    else:
        vectorstore = build_and_save_vector_db()

    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    query = "What was the revenue growth?"
    results = retriever.invoke(query)

    print(f"\nQuery: {query}")
    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc.page_content}")