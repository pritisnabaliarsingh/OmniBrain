from transformers import pipeline
from retriever import get_retriever
from prompt_templates import QA_PROMPT_V2

# Free, local model — no API key needed
generator = pipeline("text-generation", model="google/flan-t5-base")

def answer_question(query, k=2):
    """
    Full RAG pipeline: retrieve relevant chunks, build a prompt, generate an answer.
    """
    retriever = get_retriever(search_type="similarity", k=k)
    docs = retriever.invoke(query)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = QA_PROMPT_V2.format(context=context, question=query)
    result = generator(prompt, max_new_tokens=100)

    return {
        "question": query,
        "context_used": context,
        "answer": result[0]["generated_text"]
    }

if __name__ == "__main__":
    query = "What was the revenue growth?"
    result = answer_question(query)

    print(f"Question: {result['question']}\n")
    print(f"Context used:\n{result['context_used']}\n")
    print(f"Answer: {result['answer']}")