from rag_pipeline import answer_question
from response_formatter import format_response, display_response

def run_test(question, expected_behavior):
    print(f"\n--- Test: {expected_behavior} ---")
    result = answer_question(question)
    formatted = format_response(
        question=result["question"],
        answer=result["answer"],
        context_used=result["context_used"]
    )
    display_response(formatted)
    return formatted

if __name__ == "__main__":
    # Test 1: Answerable question (sanity check)
    run_test(
        "What was the revenue growth?",
        "Should answer correctly using context"
    )

    # Test 2: Unanswerable question (hallucination check)
    run_test(
        "What is the CEO's name?",
        "Should say info not available, NOT make something up"
    )

    # Test 3: Vague/nonsense question (robustness check)
    run_test(
        "asdkjaskjd random text",
        "Should not crash, should handle gracefully"
    )