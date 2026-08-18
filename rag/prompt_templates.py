from langchain_core.prompts import PromptTemplate

# Original Day 2 prompt (kept for reference/comparison)
QA_PROMPT_V1 = PromptTemplate.from_template(
    "You are a helpful assistant analyzing a document. "
    "Using only the context below, answer the question accurately. "
    "If the answer isn't in the context, say so.\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}\n\n"
    "Answer:"
)

QA_PROMPT_V2 = PromptTemplate.from_template(
    "You are a precise financial data extractor. The context below may contain a table with multiple rows.\n\n"
    "STRICT RULES:\n"
    "1. If the question mentions a specific month, region, or item name, find ONLY that exact row in the table.\n"
    "2. Do not mix up numbers between different rows.\n"
    "3. Only state facts EXACTLY as written in the context — never guess or infer.\n"
    "4. If the exact fact isn't in the context, respond exactly: 'The provided document does not contain this information.'\n"
    "5. Give a short, direct answer with the correct number only.\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}\n\n"
    "Step 1 - Identify the exact row/item the question is asking about.\n"
    "Step 2 - State the value from that exact row only.\n\n"
    "Answer:"
)
ROUTING_PROMPT = PromptTemplate.from_template(
    "Given the user query below, decide which agent should handle it:\n"
    "- 'search' for general text/document questions\n"
    "- 'sql' for numeric or historical data questions\n"
    "- 'vision' for questions about charts, tables, or images\n\n"
    "Query: {query}\n\n"
    "Respond with only one word: search, sql, or vision."
)

if __name__ == "__main__":
    context = "Q3 revenue increased by 12% compared to the previous quarter."

    print("=== V1 (Day 2) ===")
    print(QA_PROMPT_V1.format(context=context, question="What was the revenue growth?"))

    print("\n=== V2 (Tuned) ===")
    print(QA_PROMPT_V2.format(context=context, question="What was the revenue growth?"))

    print("\n=== V2 with an unanswerable question (tests hallucination guard) ===")
    print(QA_PROMPT_V2.format(context=context, question="What is the company's CEO's name?"))