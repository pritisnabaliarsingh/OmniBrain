from PIL import Image
import base64
import io
import os

def prepare_image_for_vlm(image_path: str, max_dim: int = 1024) -> str:
    """Resize + base64-encode an image so it's ready to send to GPT-4o / LLaVA."""
    img = Image.open(image_path).convert("RGB")
    img.thumbnail((max_dim, max_dim))

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded

def prepare_all_images(image_dir: str = "document_processing/output/images") -> list:
    prepared = []
    for fname in os.listdir(image_dir):
        path = os.path.join(image_dir, fname)
        encoded = prepare_image_for_vlm(path)
        prepared.append({"filename": fname, "base64": encoded})
    return prepared


if __name__ == "__main__":
    prepped = prepare_all_images()
    print(f"Prepared {len(prepped)} images for VLM")
