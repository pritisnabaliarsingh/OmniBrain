from app.utils.document_processing.pipeline.hybrid_pipeline import run_hybrid_pipeline
from app.utils.document_processing.optimize.cache import get_cached_result, save_to_cache

def run_pipeline_cached(file_path: str) -> dict:
    cached = get_cached_result(file_path)
    if cached:
        print("Loaded from cache")
        return cached

    result = run_hybrid_pipeline(file_path)
    save_to_cache(file_path, result)
    return result
