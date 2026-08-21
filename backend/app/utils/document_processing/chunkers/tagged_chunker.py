from app.utils.document_processing.chunkers.sliding_window import sliding_window_chunk

def tagged_chunks(pages: list, chunk_size: int = 300, overlap: int = 50) -> list:
    """Chunk each page's text and tag every chunk with page number + source."""
    all_chunks = []
    for page in pages:
        page_chunks = sliding_window_chunk(page["text"], chunk_size, overlap)
        for c in page_chunks:
            c["page_number"] = page["page_number"]
            c["source"] = page.get("method", "native")
            all_chunks.append(c)
    return all_chunks


if __name__ == "__main__":
    from app.utils.document_processing.extractors.text_extractor import extract_clean_pages
    pages = extract_clean_pages("document_processing/samples/sample.pdf")
    chunks = tagged_chunks(pages)
    print(f"Total tagged chunks: {len(chunks)}")
    print(chunks[0])
