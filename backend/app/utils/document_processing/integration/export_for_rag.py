import json
from app.utils.document_processing.pipeline.cached_pipeline import run_pipeline_cached

def export_for_rag(file_path: str, output_json: str = "document_processing/output/rag_input.json"):
    """
    Produces the exact JSON shape the AI/RAG agent (Vector DB + embeddings step)
    expects to consume: a flat list of {text, metadata} records.
    """
    result = run_pipeline_cached(file_path)

    rag_records = []
    for chunk in result["chunks"]:
        rag_records.append({
            "text": chunk["text"],
            "metadata": {
                "page_number": chunk["page_number"],
                "chunk_id": chunk["chunk_id"],
                "source_file": file_path,
                "extraction_method": chunk.get("source", "native")
            }
        })

    with open(output_json, "w") as f:
        json.dump(rag_records, f, indent=2)

    print(f"Exported {len(rag_records)} records to {output_json}")
    return rag_records


if __name__ == "__main__":
    export_for_rag("document_processing/samples/sample.pdf")
