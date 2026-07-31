from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

SAMPLE_DOCS = [
    "Q3 revenue increased by 12% compared to the previous quarter, driven by strong product sales.",
    "The company's total assets grew to $450 million by the end of the fiscal year.",
    "Net profit margin improved from 8% to 11% due to cost optimization measures.",
    "The board approved a new investment strategy focusing on renewable energy projects.",
]

_vectorstore_cache = None

def load_real_documents(pdf_path="document_processing/samples/sample.pdf"):
    """Loads real document chunks from Amisha's Document Processing pipeline."""
    from document_processing.integration.export_for_rag import export_for_rag
    records = export_for_rag(pdf_path)
    texts = [record["text"] for record in records]
    return texts

def get_vectorstore(documents=None, use_real_data=False):
    global _vectorstore_cache
    if _vectorstore_cache is None:
        if use_real_data:
            docs = load_real_documents()
        else:
            docs = documents if documents else SAMPLE_DOCS
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        _vectorstore_cache = FAISS.from_texts(docs, embeddings)
    return _vectorstore_cache

def get_retriever(search_type="similarity", k=2, documents=None, use_real_data=False):
    vectorstore = get_vectorstore(documents, use_real_data)
    return vectorstore.as_retriever(search_type=search_type, search_kwargs={"k": k})

if __name__ == "__main__":
    query = "What was the revenue for May?"

    print("=== Using REAL document data ===")
    retriever = get_retriever(search_type="similarity", k=3, use_real_data=True)
    for i, doc in enumerate(retriever.invoke(query), 1):
        print(f"{i}. {doc.page_content}")