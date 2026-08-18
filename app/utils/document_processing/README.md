# Document Processing Module — OmniBrain

## How to use

1. Put a real PDF at `document_processing/samples/sample.pdf`
2. Install dependencies:
   ```bash
   pip install -r document_processing/requirements.txt
   ```
3. Run the full pipeline:
   ```bash
   python -m document_processing.main document_processing/samples/sample.pdf
   ```

## Folder structure

```
document_processing/
  parsers/          -> pdf_reader.py (PyMuPDF page reading)
  chunkers/          -> sliding_window.py, tagged_chunker.py
  extractors/         -> text_extractor.py, table_extractor.py, image_extractor.py,
                          metadata_extractor.py, ocr_extractor.py, vlm_image_prep.py
  pipeline/           -> hybrid_pipeline.py, cached_pipeline.py
  optimize/           -> parallel_extract.py, cache.py
  integration/        -> export_for_rag.py (hands off to AI/RAG teammate)
  utils/              -> validators.py
  tests/              -> pytest unit tests + qa_report.py + smoke_test.py
  main.py             -> entry point, runs QA + export
  config.py           -> paths config
```

## Handoff to AI/RAG teammate

`integration/export_for_rag.py` writes `document_processing/output/rag_input.json`
— a flat list of `{text, metadata}` records ready for embedding/vector DB ingestion.

## Run tests

```bash
pytest document_processing/tests/ -v
```
