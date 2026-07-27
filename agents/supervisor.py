from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "rag"))
from rag_pipeline import answer_question
from response_formatter import format_response

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
    """Uses the LLM to decide which agent should handle the query."""
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
    return {"answer": "[SQL Agent not yet implemented by team]", "context_used": ""}

def vision_agent_placeholder(query):
    return {"answer": "[Vision Agent not yet implemented by team]", "context_used": ""}

def supervisor(query):
    """
    Main orchestrator: routes the query to the correct agent and returns a formatted answer.
    """
    agent = route_query(query)
    print(f"[Supervisor] Routed to: {agent} agent")

    if agent == "search":
        result = answer_question(query)
    elif agent == "sql":
        result = sql_agent_placeholder(query)
    elif agent == "vision":
        result = vision_agent_placeholder(query)

    formatted = format_response(
        question=query,
        answer=result["answer"],
        context_used=result.get("context_used", "")
    )
    return formatted

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