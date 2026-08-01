import sys
import os

sys.path.append(os.path.dirname(__file__))
from supervisor import supervisor

def ask_omnibrain(question: str) -> dict:
    """
    Single clean entry point for the whole AI/RAG system.
    This is what Backend/Frontend would call — no internal knowledge needed.
    """
    if not question or not question.strip():
        return {
            "question": question,
            "answer": "Please provide a valid question.",
            "confidence": "n/a"
        }

    result = supervisor(question.strip())
    return result

if __name__ == "__main__":
    print("=== OmniBrain Integration Test ===\n")

    test_questions = [
        "What was the revenue in May?",
        "Show me the sales chart",
        "Who is the CEO?",
        "",
    ]

    for q in test_questions:
        print(f"User: {q if q else '(empty)'}")
        result = ask_omnibrain(q)
        print(f"OmniBrain: {result['answer']}\n")