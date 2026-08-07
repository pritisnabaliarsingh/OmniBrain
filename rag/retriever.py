from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

_vectorstore_cache = None

def load_real_documents(pdf_path="document_processing/samples/sample.pdf"):
    """Loads real document chunks WITH metadata (page numbers, etc.) from Document Processing."""
    from document_processing.integration.export_for_rag import export_for_rag
    records = export_for_rag(pdf_path)
    # Keep text AND metadata together, instead of discarding metadata
    documents = [
        Document(page_content=r["text"], metadata=r["metadata"])
        for r in records
    ]
    return documents

def get_vectorstore(pdf_path="document_processing/samples/sample.pdf"):
    global _vectorstore_cache
    if _vectorstore_cache is None:
        documents = load_real_documents(pdf_path)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        _vectorstore_cache = FAISS.from_documents(documents, embeddings)
    return _vectorstore_cache

def get_retriever(search_type="similarity", k=2, pdf_path="document_processing/samples/sample.pdf"):
    vectorstore = get_vectorstore(pdf_path)
    return vectorstore.as_retriever(search_type=search_type, search_kwargs={"k": k})

if __name__ == "__main__":
    query = "What was the revenue for May?"
    retriever = get_retriever(search_type="similarity", k=3)
    for i, doc in enumerate(retriever.invoke(query), 1):
        page = doc.metadata.get("page_number", "unknown")
        print(f"{i}. [Page {page}] {doc.page_content}")