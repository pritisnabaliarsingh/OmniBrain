from pathlib import Path

from app.utils.document_processing.pipeline.hybrid_pipeline import (
    run_hybrid_pipeline,
)


SAMPLE_PDF = (
    Path(__file__).resolve().parent.parent
    / "samples"
    / "sample.pdf"
)


def test_pipeline_runs():
    result = run_hybrid_pipeline(str(SAMPLE_PDF))

    assert result is not None


def test_chunk_has_page_tag():
    result = run_hybrid_pipeline(str(SAMPLE_PDF))

    assert result
    assert result["chunks"]

    for chunk in result["chunks"]:
        assert isinstance(chunk, dict)
        assert "page_number" in chunk
        assert chunk["page_number"] >= 1