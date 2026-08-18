import pdfplumber

def extract_tables(file_path: str) -> list:
    results = []
    with pdfplumber.open(file_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()
            for t_idx, table in enumerate(tables):
                results.append({
                    "page_number": page_num,
                    "table_index": t_idx,
                    "rows": table
                })
    return results


if __name__ == "__main__":
    tables = extract_tables("document_processing/samples/sample.pdf")
    print(f"Found {len(tables)} tables")
    if tables:
        print(tables[0]["rows"][:3])
