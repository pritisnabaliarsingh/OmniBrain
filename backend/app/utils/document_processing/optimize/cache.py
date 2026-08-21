import hashlib
import json
import os

CACHE_DIR = "document_processing/output/cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def _file_hash(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def get_cached_result(file_path: str):
    key = _file_hash(file_path)
    cache_file = os.path.join(CACHE_DIR, f"{key}.json")
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    return None

def save_to_cache(file_path: str, result: dict):
    key = _file_hash(file_path)
    cache_file = os.path.join(CACHE_DIR, f"{key}.json")
    with open(cache_file, "w") as f:
        json.dump(result, f)
