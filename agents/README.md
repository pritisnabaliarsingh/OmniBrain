# OmniBrain — AI/RAG Module

Built by: Meghana Rose
Branch: Rag

## What this module does

This is the "thinking layer" of OmniBrain  it takes a user's question, decides which specialist agent should handle it, retrieves relevant information from real documents, and generates a grounded, hallucination-safe answer.

## Architecture

User Question
↓
Supervisor (keyword-based routing)
↓
┌──┴──┬──────────┐
Search SQL Vision
Agent Agent Agent
(built) (placeholder) (placeholder)
↓
Formatted Answer

## Key Components

| File | Purpose |
|---|---|
| `agents/main_interface.py` | **Main entry point** — `ask_omnibrain(question)` |
| `agents/supervisor.py` | Routes queries to the correct agent |
| `agents/search_agent.py` | Handles document/text questions |
| `agents/vision_prompts.py` | Prompts ready for future Vision Agent |
| `rag/retriever.py` | Real document retrieval (FAISS + embeddings) |
| `rag/rag_pipeline.py` | Full RAG pipeline (retrieve → prompt → LLM answer) |
| `rag/prompt_templates.py` | QA and routing prompts, tuned against hallucination |
| `rag/response_formatter.py` | Structures raw output into clean responses |
| `embedding_engine/` | Embedding model testing, vector DB, similarity filtering |

## How to use

```python
from agents.main_interface import ask_omnibrain

result = ask_omnibrain("What was the revenue in May?")
print(result["answer"])
```

## Tested & Verified

- ✅ Answers real questions correctly using real document data
- ✅ Refuses to hallucinate when information isn't available
- ✅ Handles empty, nonsense, and long inputs without crashing
- ✅ Routes accurately between Search, SQL, and Vision agents (100% on test cases)
- ✅ Fully integrated with Document Processing's real PDF pipeline

## Known Limitations

- SQL and Vision agents are placeholders — routing works, agent logic pending
- Uses free, local models (not GPT-4o) — works well, but a paid model would improve answer quality
- Currently configured for one sample PDF — dynamic file upload is a future enhancement

## Setup

```bash
pip install -r rag/requirements.txt
python agents/main_interface.py
```