import os
from app.utils.document_processing.pipeline.cached_pipeline import run_pipeline_cached

def smoke_test(sample_dir: str = "document_processing/samples"):
    pdfs = [f for f in os.listdir(sample_dir) if f.endswith(".pdf")]
    failures = []
    for pdf in pdfs:
        path = os.path.join(sample_dir, pdf)
        try:
            result = run_pipeline_cached(path)
            assert result["total_chunks"] > 0
            print(f"[OK] {pdf} -> {result['total_chunks']} chunks")
        except Exception as e:
            failures.append((pdf, str(e)))
            print(f"[FAIL] {pdf} -> {e}")
    return failures

if __name__ == "__main__":
    smoke_test()
