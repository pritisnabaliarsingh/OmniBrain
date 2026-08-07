def format_response(question, answer, context_used, sources=None, source_pages=None):
    """
    Takes raw pipeline output and formats it into a clean, structured response
    ready for the frontend to display.
    """
    cleaned_answer = answer.strip()
    if not cleaned_answer:
        cleaned_answer = "The provided document does not contain this information."

    formatted = {
        "question": question,
        "answer": cleaned_answer,
        "sources_used": sources if sources else ["Document Processing Pipeline (real extracted data)"],
        "source_pages": source_pages if source_pages else [],
        "context_snippet": context_used[:200] + ("..." if len(context_used) > 200 else ""),
        "confidence": "high" if len(cleaned_answer) > 0 and "does not contain" not in cleaned_answer else "low"
    }
    return formatted

def display_response(formatted_response):
    """Pretty-prints a formatted response for testing/demo purposes."""
    print(f"Q: {formatted_response['question']}")
    print(f"A: {formatted_response['answer']}")
    print(f"Confidence: {formatted_response['confidence']}")
    if formatted_response.get('source_pages'):
        print(f"Source page(s): {formatted_response['source_pages']}")
    print(f"Sources: {', '.join(formatted_response['sources_used'])}")

if __name__ == "__main__":
    from rag_pipeline import answer_question
    result = answer_question("What was the revenue growth?")
    formatted = format_response(
        question=result["question"],
        answer=result["answer"],
        context_used=result["context_used"]
    )
    display_response(formatted)