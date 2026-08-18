def sliding_window_chunk(text: str, chunk_size: int = 500, overlap: int = 100) -> list:
    """
    Splits text into overlapping chunks (word-based).
    chunk_size and overlap are in words, not characters.
    """
    words = text.split()
    chunks = []
    start = 0
    chunk_id = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunks.append({
            "chunk_id": chunk_id,
            "text": " ".join(chunk_words),
            "start_word": start,
            "end_word": min(end, len(words))
        })
        chunk_id += 1
        start += (chunk_size - overlap)

    return chunks


if __name__ == "__main__":
    sample_text = "This is a test sentence. " * 200
    result = sliding_window_chunk(sample_text, chunk_size=50, overlap=10)
    print(f"Total chunks: {len(result)}")
    print(result[0])
