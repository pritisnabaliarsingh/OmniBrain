import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "rag"))
from search_agent import search_agent
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

ROUTING_PROMPT_TEXT = (
    "Given the user query below, decide which agent should handle it:\n"
    "- 'search' for general text/document questions\n"
    "- 'sql' for numeric or historical data questions\n"
    "- 'vision' for questions about charts, tables, or images\n\n"
    "Query: {query}\n\n"
    "Respond with only one word: search, sql, or vision."
)

def route_query(query):
    prompt = ROUTING_PROMPT_TEXT.format(query=query)
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=10)
    decision = tokenizer.decode(outputs[0], skip_special_tokens=True).strip().lower()

    if "sql" in decision:
        return "sql"
    elif "vision" in decision:
        return "vision"
    else:
        return "search"

def sql_agent_placeholder(query):
    return {"question": query, "answer": "[SQL Agent not yet implemented by team]", "confidence": "n/a"}

def vision_agent_placeholder(query):
    return {"question": query, "answer": "[Vision Agent not yet implemented by team]", "confidence": "n/a"}

def supervisor(query):
    agent = route_query(query)
    print(f"[Supervisor] Routed to: {agent} agent")

    if agent == "search":
        return search_agent(query)
    elif agent == "sql":
        return sql_agent_placeholder(query)
    elif agent == "vision":
        return vision_agent_placeholder(query)

if __name__ == "__main__":
    test_queries = [
        "What was the revenue growth?",
        "Show me the sales chart",
        "What is the SQL database schema?",
    ]

    for q in test_queries:
        print(f"\n=== Query: {q} ===")
        result = supervisor(q)
        print(f"Answer: {result['answer']}")