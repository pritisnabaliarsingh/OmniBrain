import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "rag"))
from search_agent import search_agent
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Keyword-based routing — fast, reliable, no model needed for obvious cases
VISION_KEYWORDS = ["chart", "image", "picture", "graph", "diagram", "photo", "visual", "figure", "table image"]
SQL_KEYWORDS = ["database", "schema", "sql", "table structure", "column", "query the database", "records in database"]

def route_query(query):
    """
    Hybrid routing: keyword rules first (fast, accurate),
    LLM classification as fallback for ambiguous cases.
    """
    query_lower = query.lower().strip()

    if not query_lower:
        return "search"  # default for empty input

    # Rule 1: Check for vision keywords
    if any(keyword in query_lower for keyword in VISION_KEYWORDS):
        return "vision"

    # Rule 2: Check for SQL keywords
    if any(keyword in query_lower for keyword in SQL_KEYWORDS):
        return "sql"

   # Rule 3: No clear keyword match — default to Search Agent (the reliable, working agent)
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
        "What was the revenue in May?",
        "Show me the sales chart",
        "What is the SQL database schema?",
        "Who is the CEO?",
    ]

    for q in test_queries:
        print(f"\n=== Query: {q} ===")
        result = supervisor(q)
        print(f"Answer: {result['answer']}")