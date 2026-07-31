from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from document_processing.integration.export_for_rag import export_for_rag

def get_real_documents(pdf_path="document_processing/samples/sample.pdf"):
    records = export_for_rag(pdf_path)
    return [r["text"] for r in records]

def search_with_threshold(query, documents=None, threshold=0.3, max_results=3):
    docs = documents if documents else get_real_documents()
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(docs, embeddings)

    results = vectorstore.similarity_search_with_score(query, k=max_results)

    filtered = []
    for doc, score in results:
        similarity = 1 / (1 + score)
        if similarity >= threshold:
            filtered.append((doc.page_content, round(similarity, 4)))

    return filtered

if __name__ == "__main__":
    query = "What was the revenue in May?"
    results = search_with_threshold(query, threshold=0.3)

    print(f"Query: {query}\n")
    if results:
        print("Relevant results (above threshold):")
        for text, score in results:
            print(f"- ({score}) {text}")
    else:
        print("No sufficiently relevant results found.")