from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
import sys
import os
import re

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

_vectorstore_cache = None

def reformat_table_text(text):
    """
    Detects table-like text (Month Region Units Revenue...) and reformats it
    into clear one-row-per-line format, so numbers can't be confused with the wrong column.
    """
    if "Month" in text and "Region" in text and "Revenue" in text:
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        pattern = r'(' + '|'.join(months) + r')\s+(\w+)\s+(\d+)\s+(\d+)'
        matches = re.findall(pattern, text)
        if matches:
            lines = ["Sales data by month:"]
            for month, region, units, revenue in matches:
                lines.append(f"- Month: {month}, Region: {region}, Units Sold: {units}, Revenue (USD): {revenue}")
            return "\n".join(lines)
    return text

def load_real_documents(pdf_path="document_processing/samples/sample.pdf"):
    """Loads real document chunks WITH metadata (page numbers, etc.) from Document Processing."""
    from document_processing.integration.export_for_rag import export_for_rag
    records = export_for_rag(pdf_path)
    documents = [
        Document(page_content=reformat_table_text(r["text"]), metadata=r["metadata"])
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