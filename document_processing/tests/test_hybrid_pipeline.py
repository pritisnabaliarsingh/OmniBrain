from document_processing.pipeline.hybrid_pipeline import run_hybrid_pipeline

def test_pipeline_runs():
    result = run_hybrid_pipeline("document_processing/samples/sample.pdf")
    assert "chunks" in result
    assert result["total_chunks"] > 0

def test_chunk_has_page_tag():
    result = run_hybrid_pipeline("document_processing/samples/sample.pdf")
    for c in result["chunks"][:5]:
        assert "page_number" in c
