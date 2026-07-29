from document_processing.chunkers.sliding_window import sliding_window_chunk

def test_chunk_count():
    text = "word " * 1000
    chunks = sliding_window_chunk(text, chunk_size=100, overlap=20)
    assert len(chunks) > 1

def test_overlap_correctness():
    text = "word " * 300
    chunks = sliding_window_chunk(text, chunk_size=100, overlap=20)
    assert chunks[1]["start_word"] < chunks[0]["end_word"]

def test_empty_text():
    chunks = sliding_window_chunk("", chunk_size=100, overlap=20)
    assert chunks == []
