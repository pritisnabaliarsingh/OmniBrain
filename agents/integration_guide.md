# AI/RAG Module — Integration Guide (for Backend team)

## How to use this module

```python
from agents.main_interface import ask_omnibrain

result = ask_omnibrain("What was the revenue in May?")
print(result["answer"])
```

## Function signature

`ask_omnibrain(question: str) -> dict`

**Input:** A plain text question (string)

**Output:** A dictionary with these keys:
- `question` — the original question asked
- `answer` — the AI-generated answer (string)
- `confidence` — "high", "low", or "n/a"
- `sources_used` — list of sources referenced (may not exist for placeholder agents)

## Example response

```json
{
  "question": "What was the revenue in May?",
  "answer": "200 21000.",
  "confidence": "high",
  "sources_used": ["Document Processing Pipeline (real extracted data)"]
}
```

## Notes for Backend integration
- Currently processes a single hardcoded sample PDF (`document_processing/samples/sample.pdf`) — dynamic file upload support would need a small change to accept a file path parameter
- SQL and Vision agents are placeholders — routing works, but they return "not yet implemented" messages until built
- No API key or environment variables required — runs on free, local models