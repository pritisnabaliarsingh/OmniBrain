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

# Tuned version — more specific instructions, reduces hallucination risk
QA_PROMPT_V2 = PromptTemplate.from_template(
    "You are a financial document analyst. Follow these rules strictly:\n"
    "1. Only use information explicitly stated in the context below.\n"
    "2. If the context does not contain the answer, respond exactly with: "
    "'The provided document does not contain this information.'\n"
    "3. Keep your answer concise — 1 to 3 sentences maximum.\n"
    "4. Do not guess, assume, or add outside knowledge.\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}\n\n"
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