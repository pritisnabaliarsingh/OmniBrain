import fitz
import os

def extract_images(file_path: str, output_dir: str = "document_processing/output/images") -> list:
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(file_path)
    extracted = []

    for page_num, page in enumerate(doc, start=1):
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            filename = f"page{page_num}_img{img_index}.{ext}"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "wb") as f:
                f.write(image_bytes)
            extracted.append({"page_number": page_num, "path": filepath})

    doc.close()
    return extracted


if __name__ == "__main__":
    imgs = extract_images("document_processing/samples/sample.pdf")
    print(f"Extracted {len(imgs)} images")
