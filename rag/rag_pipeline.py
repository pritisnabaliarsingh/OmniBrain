from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from retriever import get_retriever
from prompt_templates import QA_PROMPT_V2

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

def answer_question(query, k=2):
    retriever = get_retriever(search_type="similarity", k=k)
    docs = retriever.invoke(query)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = QA_PROMPT_V2.format(context=context, question=query)
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=100)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {
        "question": query,
        "context_used": context,
        "answer": answer
    }
if __name__ == "__main__":
    test_queries = [
        "What was the revenue in May?",
        "Who is the CEO of the company?",
    ]

    for query in test_queries:
        result = answer_question(query)
        print(f"\nQuestion: {result['question']}")
        print(f"Answer: {result['answer']}")