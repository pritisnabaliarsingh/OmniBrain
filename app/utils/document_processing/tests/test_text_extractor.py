from app.utils.document_processing.extractors.text_extractor import clean_text

def test_whitespace_collapse():
    assert clean_text("hello    world\n\n\n") == "hello world"

def test_hyphen_fix():
    assert clean_text("infor-\nmation") == "information"
