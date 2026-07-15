from langchain_core.prompts import PromptTemplate

QA_PROMPT = PromptTemplate.from_template(
    "You are a helpful assistant analyzing a document. "
    "Using only the context below, answer the question accurately. "
    "If the answer isn't in the context, say so.\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}\n\n"
    "Answer:"
)
#deciding which agent should handle a query
ROUTING_PROMPT = PromptTemplate.from_template(
    "Given the user query below, decide which agent should handle it:\n"
    "- 'search' for general text/document questions\n"
    "- 'sql' for numeric or historical data questions\n"
    "- 'vision' for questions about charts, tables, or images\n\n"
    "Query: {query}\n\n"
    "Respond with only one word: search, sql, or vision."
)
if __name__ == "__main__":
    print(QA_PROMPT.format(context="Sample document text about Q3 revenue.", question="What was Q3 revenue?"))
    print("\n---\n")
    print(ROUTING_PROMPT.format(query="Show me the sales chart for last quarter"))
