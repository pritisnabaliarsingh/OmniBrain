from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
try:
    from rag.retriever import get_retriever
    from rag.prompt_templates import QA_PROMPT_V2
except ModuleNotFoundError:
    from retriever import get_retriever
    from prompt_templates import QA_PROMPT_V2

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

def answer_question(query, k=2):
    retriever = get_retriever(search_type="similarity", k=k)
    docs = retriever.invoke(query)
    context = "\n".join([doc.page_content for doc in docs])
    pages = sorted(set(doc.metadata.get("page_number", "unknown") for doc in docs))

    prompt = QA_PROMPT_V2.format(context=context, question=query)
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=100)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {
        "question": query,
        "context_used": context,
        "answer": answer,
        "source_pages": pages
    }

if __name__ == "__main__":
    query = "What was the revenue in May?"
    result = answer_question(query)
    print(f"Question: {result['question']}")
    print(f"Answer: {result['answer']}")
    print(f"Source page(s): {result['source_pages']}")