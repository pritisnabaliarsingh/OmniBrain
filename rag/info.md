# Module Information

Developer Name: Meghana Rose
Branch Name: Rag
Module Name: AI/RAG


## Install Command

```bash
pip install -r requirements.txt
```

## Run Command

```bash
python agents/main_interface.py
```

## Port Number

Not Applicable

## Environment Variables

None

## Additional Notes

- Uses HuggingFace sentence-transformers for embeddings (runs locally, no API key required)
- Fully integrated with real document data via the Document Processing module (no longer uses placeholder sample data)
- Main entry point is `ask_omnibrain()` in `agents/main_interface.py`