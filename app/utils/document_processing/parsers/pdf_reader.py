import fitz  # PyMuPDF

class PDFReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.doc = fitz.open(file_path)

    def page_count(self) -> int:
        return len(self.doc)

    def get_page_text(self, page_num: int) -> str:
        return self.doc[page_num].get_text()

    def get_all_pages_text(self) -> list:
        return [page.get_text() for page in self.doc]

    def close(self):
        self.doc.close()


if __name__ == "__main__":
    reader = PDFReader("document_processing/samples/sample.pdf")
    print(f"Pages: {reader.page_count()}")
    print(reader.get_page_text(0)[:500])
    reader.close()
