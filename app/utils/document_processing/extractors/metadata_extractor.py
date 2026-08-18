import fitz

def extract_metadata(file_path: str) -> dict:
    doc = fitz.open(file_path)
    meta = doc.metadata
    toc = doc.get_toc()  # table of contents / sections

    result = {
        "title": meta.get("title"),
        "author": meta.get("author"),
        "page_count": len(doc),
        "sections": [{"level": t[0], "title": t[1], "page": t[2]} for t in toc]
    }
    doc.close()
    return result


if __name__ == "__main__":
    meta = extract_metadata("document_processing/samples/sample.pdf")
    print(meta)
