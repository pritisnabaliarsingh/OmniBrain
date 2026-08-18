import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from rag.rag_pipeline import answer_question
from rag.response_formatter import format_response

def search_agent(query, k=2):
    result = answer_question(query, k=k)

    # Safety check: if the retrieved context has low overlap with the question's
    # key words, don't trust the AI's answer - it's likely guessing
    context_lower = result["context_used"].lower()
    query_words = [w for w in query.lower().split() if len(w) > 4]  # skip short words like "the", "was"
    matches = sum(1 for w in query_words if w in context_lower)

    if query_words and matches == 0:
        # None of the question's key words appear in the retrieved text at all
        result["answer"] = "The provided document does not contain this information."

    formatted = format_response(
        question=result["question"],
        answer=result["answer"],
        context_used=result["context_used"],
        sources=["Document Search (real data)"],
        source_pages=result.get("source_pages", [])
    )
    return formatted

if __name__ == "__main__":
    test_queries = [
        "What was the revenue growth?",
        "What is the total assets value?",
        "What is the CEO's name?",
        "What was the revenue in May?",
    ]

    for q in test_queries:
        print(f"\n=== Query: {q} ===")
        result = search_agent(q)
        print(f"Answer: {result['answer']}")
        print(f"Confidence: {result['confidence']}")