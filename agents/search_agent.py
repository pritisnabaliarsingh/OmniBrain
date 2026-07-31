import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from rag.rag_pipeline import answer_question
from rag.response_formatter import format_response

def search_agent(query, k=2):
    """
    Search Agent — handles general text/document questions.
    Wraps the RAG pipeline (retriever + prompt + LLM) into a clean, standard interface
    that the Supervisor can call.
    """
    result = answer_question(query, k=k)
    formatted = format_response(
        question=result["question"],
        answer=result["answer"],
        context_used=result["context_used"],
        sources=["Document Search (sample data)"]
    )
    return formatted

if __name__ == "__main__":
    test_queries = [
        "What was the revenue growth?",
        "What is the total assets value?",
        "What is the CEO's name?",
    ]

    for q in test_queries:
        print(f"\n=== Query: {q} ===")
        result = search_agent(q)
        print(f"Answer: {result['answer']}")
        print(f"Confidence: {result['confidence']}")